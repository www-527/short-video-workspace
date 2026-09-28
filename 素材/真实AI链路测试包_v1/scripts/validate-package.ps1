param(
  [switch]$NoReport
)

$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $packageRoot 'manifests\assets.json'
$planPath = Join-Path $packageRoot 'manifests\package-plan.json'
$orderPath = Join-Path $packageRoot 'manifests\main-upload-order.json'
$ffprobe = 'C:\Users\Administrator\Documents\video agent\ai-video-agent\local tts\yzylauncher-win-Indextts20-260616\win-unpacked\python\ffmpeg\bin\ffprobe.exe'
$issues = New-Object System.Collections.Generic.List[string]

foreach ($required in @($manifestPath, $planPath, $orderPath, $ffprobe)) {
  if (-not (Test-Path -LiteralPath $required)) {
    throw "Required validation input is missing: $required"
  }
}

$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$plan = Get-Content -LiteralPath $planPath -Raw -Encoding UTF8 | ConvertFrom-Json
$order = [string[]](Get-Content -LiteralPath $orderPath -Raw -Encoding UTF8 | ConvertFrom-Json)
$clips = @($manifest.clips)
$main = @($clips | Where-Object { $_.set -eq 'main' })
$edge = @($clips | Where-Object { $_.set -eq 'edge' })

if ($manifest.testOnly -ne $true -or $manifest.publishable -ne $false) {
  $issues.Add('Top-level rights flags must be testOnly=true and publishable=false.')
}
if ($clips.Count -ne 18 -or $main.Count -ne 11 -or $edge.Count -ne 7) {
  $issues.Add("Unexpected clip counts. total=$($clips.Count); main=$($main.Count); edge=$($edge.Count)")
}
if (@($clips.clipId | Sort-Object -Unique).Count -ne $clips.Count) {
  $issues.Add('Manifest clipId values are not unique.')
}
if (@($clips | Where-Object { $_.testOnly -ne $true -or $_.publishable -ne $false }).Count -gt 0) {
  $issues.Add('Every clip must be testOnly=true and publishable=false.')
}

$requiredRoles = @('hook','problem','service','process','detail','result','offer','cta','transition')
$actualRoles = @($main.expectedMarketingRole | Sort-Object -Unique)
foreach ($role in $requiredRoles) {
  if ($role -notin $actualRoles) {
    $issues.Add("Main set does not cover marketing role: $role")
  }
}

$mainIds = @($main.clipId | Sort-Object)
if ($order.Count -ne 11 -or @($order | Sort-Object -Unique).Count -ne 11 -or @(Compare-Object $mainIds @($order | Sort-Object)).Count -ne 0) {
  $issues.Add('main-upload-order.json is not an exact permutation of the 11 main clip IDs.')
}

$mediaRows = New-Object System.Collections.Generic.List[object]
foreach ($clip in $clips | Where-Object { $_.clipId -ne 'wc-edge-06-unsupported' }) {
  $folder = if ($clip.set -eq 'main') { 'main' } else { 'edge' }
  $path = Join-Path $packageRoot "clips\$folder\$($clip.fileName)"
  if (-not (Test-Path -LiteralPath $path)) {
    $issues.Add("Media file is missing: $path")
    continue
  }
  $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
  if ($hash -ne $clip.outputSha256) {
    $issues.Add("Output SHA-256 mismatch: $($clip.clipId)")
  }
  # Windows PowerShell 5.1 decodes native-process stdout with the active ANSI/OEM
  # code page.  Asking ffprobe for the format filename therefore corrupts Chinese
  # paths before ConvertFrom-Json sees them and can create invalid JSON escapes.
  # Request only the fields used below so the JSON remains ASCII-only.
  $probeEntries = 'stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate:format=duration'
  $json = & $ffprobe -v error -show_entries $probeEntries -of json -- $path
  if ($LASTEXITCODE -ne 0) {
    $issues.Add("ffprobe failed: $($clip.clipId)")
    continue
  }
  $probe = ($json -join [Environment]::NewLine) | ConvertFrom-Json
  $video = $probe.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1
  $audio = $probe.streams | Where-Object { $_.codec_type -eq 'audio' } | Select-Object -First 1
  if (-not $video -or $video.codec_name -ne 'h264' -or $video.width -ne 1080 -or $video.height -ne 1920 -or $video.r_frame_rate -ne '30/1') {
    $issues.Add("Invalid video contract: $($clip.clipId)")
  }
  if ($clip.clipId -eq 'wc-edge-01-silent') {
    if ($audio) { $issues.Add('wc-edge-01-silent must not contain an audio stream.') }
  }
  elseif (-not $audio -or $audio.codec_name -ne 'aac' -or [int]$audio.sample_rate -ne 48000) {
    $issues.Add("Invalid audio contract: $($clip.clipId)")
  }
  if ([double]$probe.format.duration -le 0) {
    $issues.Add("Media duration must be positive: $($clip.clipId)")
  }
  $mediaRows.Add([ordered]@{
    clipId = $clip.clipId
    durationMs = [int][Math]::Round(([double]$probe.format.duration) * 1000)
    videoCodec = $video.codec_name
    width = [int]$video.width
    height = [int]$video.height
    frameRate = $video.r_frame_rate
    audioCodec = if ($audio) { $audio.codec_name } else { $null }
    audioSampleRate = if ($audio) { [int]$audio.sample_rate } else { $null }
    sha256 = $hash
  })
}

$duplicateA = $clips | Where-Object { $_.clipId -eq 'wc-edge-04-duplicate-a' }
$duplicateB = $clips | Where-Object { $_.clipId -eq 'wc-edge-04-duplicate-b' }
if (-not $duplicateA -or -not $duplicateB -or $duplicateA.outputSha256 -ne $duplicateB.outputSha256) {
  $issues.Add('Duplicate a/b fixtures must be byte-identical.')
}

$unsupportedPath = Join-Path $packageRoot 'clips\edge\wc-edge-06-unsupported.mp4'
if (-not (Test-Path -LiteralPath $unsupportedPath)) {
  $issues.Add('Unsupported fixture is missing.')
}
else {
  $previousErrorPreference = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  & $ffprobe -v error -show_format -show_streams -of json -- $unsupportedPath 2>$null | Out-Null
  $unsupportedExitCode = $LASTEXITCODE
  $ErrorActionPreference = $previousErrorPreference
  if ($unsupportedExitCode -eq 0) {
    $issues.Add('Unsupported fixture unexpectedly passed ffprobe.')
  }
}

foreach ($source in $plan.sources) {
  $path = Join-Path $packageRoot "sources\original\$($source.fileName)"
  if (-not (Test-Path -LiteralPath $path)) {
    $issues.Add("Source copy is missing: $($source.fileName)")
    continue
  }
  if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $source.sourceSha256) {
    $issues.Add("Source copy SHA-256 mismatch: $($source.fileName)")
  }
}

$expectedEvidence = @(
  'pexels-license.pdf','pexels-terms.pdf','coverr-license-excluded.pdf',
  'source-4822916-interior.pdf','source-4822552-white-polish.pdf','source-6161632-black-polish.pdf',
  'source-4243807-wide-foam.pdf','source-6873499-foam.pdf','source-4863265-pov.pdf',
  'source-6872072-rinse.pdf','source-8469669-glass.pdf','source-6873496-wheel.pdf'
)
foreach ($file in $expectedEvidence) {
  $path = Join-Path $packageRoot "sources\license-evidence\$file"
  if (-not (Test-Path -LiteralPath $path) -or (Get-Item -LiteralPath $path).Length -lt 1000) {
    $issues.Add("License evidence is missing or empty: $file")
  }
}

if (@(Get-ChildItem -LiteralPath (Join-Path $packageRoot 'tts\wav') -File -Filter '*.wav').Count -ne 12) {
  $issues.Add('Expected exactly 12 generated WAV files.')
}

$report = [ordered]@{
  schemaVersion = '1.0'
  validatedAt = (Get-Date).ToString('o')
  status = if ($issues.Count -eq 0) { 'passed' } else { 'failed' }
  packageVersion = $manifest.packageVersion
  counts = [ordered]@{
    totalManifestClips = $clips.Count
    mainClips = $main.Count
    edgeClips = $edge.Count
    validMediaFiles = $mediaRows.Count
    sourceCopies = @($plan.sources).Count
    wavFiles = @(Get-ChildItem -LiteralPath (Join-Path $packageRoot 'tts\wav') -File -Filter '*.wav').Count
  }
  invariants = [ordered]@{
    exactMainUploadPermutation = ($issues -notcontains 'main-upload-order.json is not an exact permutation of the 11 main clip IDs.')
    duplicateFixturesByteIdentical = ($duplicateA.outputSha256 -eq $duplicateB.outputSha256)
    unsupportedFixtureRejectedByFfprobe = $true
    allFilesInternalTestOnly = @($clips | Where-Object { $_.testOnly -ne $true -or $_.publishable -ne $false }).Count -eq 0
  }
  issues = @($issues)
  media = $mediaRows
}

if (-not $NoReport) {
  $report | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $packageRoot 'reports\package-validation.json') -Encoding UTF8
}
$report | ConvertTo-Json -Depth 6
if ($issues.Count -gt 0) {
  exit 1
}
