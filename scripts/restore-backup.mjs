// Run only in a newly extracted, offline backup. Requires Node.js 24+.
import {readFile, writeFile, readdir, stat} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {DatabaseSync} from 'node:sqlite';
import {createHash, createDecipheriv} from 'node:crypto';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const manifestPath = path.join(root, 'backup-manifest.json');
const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
const oldRoot = manifest.restoredRoot ?? manifest.sourceRoot;
const relocate = process.argv.includes('--relocate');
const data = path.join(root, 'washcut-agent-demo', 'data');
const database = path.join(data, 'washcut.sqlite');
const quote = (name) => '"' + name.replaceAll('"', '""') + '"';
const normalize = (value) => value.replaceAll('\\', '/').replace(/\/$/, '');
const sameRoot = normalize(root).toLowerCase() === normalize(oldRoot).toLowerCase();

function rebase(value) {
  if (typeof value === 'string') {
    const normalized = normalize(value);
    const prefix = normalize(oldRoot);
    if (normalized.toLowerCase().startsWith(prefix.toLowerCase() + '/')) {
      return path.join(root, ...normalized.slice(prefix.length + 1).split('/'));
    }
    return value;
  }
  if (Array.isArray(value)) return value.map(rebase);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([key, entry]) => [key, rebase(entry)]));
  }
  return value;
}

async function* files(directory) {
  for (const entry of await readdir(directory, {withFileTypes: true})) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) yield* files(target);
    else if (entry.isFile()) yield target;
  }
}

if (relocate && !sameRoot) {
  // This command is for a fresh extraction; never run with the application open.
  // SQLite changes are transactional. Files are idempotently rebased, so retrying
  // after interruption completes remaining changes without replacing user data.
  const db = new DatabaseSync(database);
  try {
    db.exec('BEGIN IMMEDIATE');
    const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").all();
    for (const {name} of tables) {
      const columns = db.prepare(`PRAGMA table_info(${quote(name)})`).all().filter((column) => column.type === 'TEXT');
      for (const row of db.prepare(`SELECT rowid AS backup_row_id, * FROM ${quote(name)}`).all()) {
        for (const {name: column} of columns) {
          const original = row[column];
          if (typeof original !== 'string') continue;
          let changed;
          if (column.endsWith('_json')) {
            const parsed = JSON.parse(original);
            const rebased = rebase(parsed);
            changed = JSON.stringify(rebased) === JSON.stringify(parsed) ? original : JSON.stringify(rebased);
          } else {
            changed = rebase(original);
          }
          if (changed !== original) db.prepare(`UPDATE ${quote(name)} SET ${quote(column)}=? WHERE rowid=?`).run(changed, row.backup_row_id);
        }
      }
    }
    db.exec('COMMIT');
  } catch (error) {
    if (db.isTransaction) db.exec('ROLLBACK');
    throw error;
  } finally {
    db.close();
  }
  for await (const file of files(data)) {
    if (!file.endsWith('.json')) continue;
    const original = await readFile(file, 'utf8');
    const parsed = JSON.parse(original.replace(/^\uFEFF/, ''));
    const rebased = rebase(parsed);
    if (JSON.stringify(parsed) !== JSON.stringify(rebased)) await writeFile(file, JSON.stringify(rebased, null, 2) + '\n');
  }
  for (const relative of ['washcut-agent-demo/.env', 'washcut-agent-demo/qwen3-asr-gateway/.env']) {
    const file = path.join(root, relative);
    const original = await readFile(file, 'utf8');
    const changed = original.replace(/^(\s*[A-Z_]+\s*=)([^\r\n]*)/gm, (line, prefix, value) => {
      const trimmed = value.trim();
      const quoted = (trimmed.startsWith('"') && trimmed.endsWith('"')) || (trimmed.startsWith("'") && trimmed.endsWith("'"));
      const unquoted = quoted ? trimmed.slice(1, -1) : trimmed;
      const rebased = rebase(unquoted);
      return rebased === unquoted ? line : prefix + (quoted ? trimmed[0] + rebased + trimmed[0] : rebased);
    });
    if (changed !== original) await writeFile(file, changed);
  }
  manifest.restoredRoot = root;
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
  console.log('Paths relocated to:', root);
} else if (!sameRoot) {
  throw new Error('The backup is in a different folder. Before starting the app, run: node scripts/restore-backup.mjs --relocate');
}

const db = new DatabaseSync(database, {readOnly: true});
try {
  const integrity = db.prepare('PRAGMA integrity_check').all();
  if (integrity.length !== 1 || integrity[0].integrity_check !== 'ok') throw new Error(JSON.stringify(integrity));
  const assets = db.prepare('SELECT payload_json FROM auto_video_assets').all().map((row) => JSON.parse(row.payload_json));
  const missing = [];
  for (const asset of assets) {
    try {
      const info = await stat(asset.originalPath);
      if (info.size !== asset.fileSize) missing.push({assetId: asset.id, reason: 'size_mismatch', path: asset.originalPath});
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
      missing.push({assetId: asset.id, reason: 'missing', path: asset.originalPath});
    }
  }
  const generations = db.prepare("SELECT * FROM auto_video_generations WHERE status='completed'").all();
  for (const generation of generations) {
    const projectDirectory = path.join(data, 'auto-video', 'projects', generation.project_id);
    const directory = generation.artifact_storage === 'project' ? projectDirectory : path.join(projectDirectory, 'generations', generation.generation_id);
    const output = JSON.parse(generation.output_json);
    for (const [name, expected] of [['output.mp4', output.fileSize], ['output-captioned.mp4', output.captionedFileSize]]) {
      if (expected === undefined && name === 'output-captioned.mp4') continue;
      const file = path.join(directory, name);
      try {
        const info = await stat(file);
        if (expected !== undefined && info.size !== expected) missing.push({path: file, reason: 'size_mismatch'});
      } catch (error) {
        if (error.code !== 'ENOENT') throw error;
        missing.push({path: file, reason: 'missing'});
      }
    }
  }
  const environment = path.join(root, 'washcut-agent-demo', '.env');
  process.loadEnvFile(environment);
  const secret = process.env.KEY_ENCRYPTION_SECRET?.trim() || (await readFile(path.join(data, '.relay-key-secret'), 'utf8')).trim();
  const encryptionKey = createHash('sha256').update(secret).digest();
  const keys = db.prepare('SELECT encrypted_api_key FROM relay_keys').all();
  for (const {encrypted_api_key: encrypted} of keys) {
    const [version, iv, tag, value] = encrypted.split(':');
    if (version !== 'v1') throw new Error('relay_key_ciphertext_invalid');
    const decipher = createDecipheriv('aes-256-gcm', encryptionKey, Buffer.from(iv, 'base64url'));
    decipher.setAuthTag(Buffer.from(tag, 'base64url'));
    decipher.update(Buffer.from(value, 'base64url'));
    decipher.final(); // Authenticate without printing any credentials.
  }
  for (const model of ['qwen3-asr-1.7b', 'qwen3-forced-aligner-0.6b']) {
    const directory = path.join(root, 'model', model);
    await stat(path.join(directory, 'config.json'));
    const weights = (await readdir(directory)).filter((name) => name.endsWith('.safetensors'));
    if (!weights.length) throw new Error('Missing model weights: ' + model);
  }
  console.log(JSON.stringify({integrity: 'ok', projects: db.prepare('SELECT COUNT(*) AS count FROM auto_video_projects').get().count, assets: assets.length, completedGenerations: generations.length, decryptedConnections: keys.length, missing}, null, 2));
  if (missing.length) process.exitCode = 1;
} finally {
  db.close();
}
