param(
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$workspaceRoot = Split-Path -Parent (Split-Path -Parent $packageRoot)
$repoRoot = Join-Path $workspaceRoot 'washcut-agent-demo'
$sourceRoot = Join-Path $repoRoot '素材_洗车可商用'
$planPath = Join-Path $packageRoot 'manifests\package-plan.json'
$wavDir = Join-Path $packageRoot 'tts\wav'
$mainDir = Join-Path $packageRoot 'clips\main'
$edgeDir = Join-Path $packageRoot 'clips\edge'
$probeDir = Join-Path $packageRoot 'probe'
$originalDir = Join-Path $packageRoot 'sources\original'
$ffmpegRoot = 'C:\Users\Administrator\Documents\video agent\ai-video-agent\local tts\yzylauncher-win-Indextts20-260616\win-unpacked\python\ffmpeg\bin'
$ffmpeg = Join-Path $ffmpegRoot 'ffmpeg.exe'
$ffprobe = Join-Path $ffmpegRoot 'ffprobe.exe'
$fontPath = 'C\:/Windows/Fonts/msyh.ttc'

foreach ($required in @($planPath, $ffmpeg, $ffprobe, 'C:\Windows\Fonts\msyh.ttc')) {
  if (-not (Test-Path -LiteralPath $required)) {
    throw "Required file is missing: $required"
  }
}

New-Item -ItemType Directory -Path $mainDir, $edgeDir, $probeDir, $originalDir -Force | Out-Null
$plan = Get-Content -LiteralPath $planPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sourceByKey = @{}
foreach ($source in $plan.sources) {
  $sourceByKey[$source.key] = $source
  $sourcePath = Join-Path $sourceRoot $source.fileName
  if (-not (Test-Path -LiteralPath $sourcePath)) {
    throw "Source file is missing: $sourcePath"
  }
  $actualHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
  if ($actualHash -ne $source.sourceSha256) {
    throw "Source SHA-256 mismatch for $($source.fileName). expected=$($source.sourceSha256); actual=$actualHash"
  }
  $copyPath = Join-Path $originalDir $source.fileName
  if ($Force -or -not (Test-Path -LiteralPath $copyPath)) {
    Copy-Item -LiteralPath $sourcePath -Destination $copyPath -Force
    (Get-Item -LiteralPath $copyPath).IsReadOnly = $true
  }
}

function Invoke-Ffmpeg {
  param([Parameter(Mandatory = $true)][string[]]$Arguments)
  $output = & $ffmpeg @Arguments 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "FFmpeg failed (exit=$LASTEXITCODE).`n$($output -join [Environment]::NewLine)"
  }
}

function Get-AudioDurationSeconds {
  param([Parameter(Mandatory = $true)][string]$Path)
  $value = & $ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -- $Path
  if ($LASTEXITCODE -ne 0 -or -not $value) {
    throw "Unable to read audio duration: $Path"
  }
  return [double]::Parse($value.Trim(), [Globalization.CultureInfo]::InvariantCulture)
}

function Get-MediaProbe {
  param(
    [Parameter(Mandatory = $true)][string]$ClipId,
    [Parameter(Mandatory = $true)][string]$Path
  )
  $json = & $ffprobe -v error -show_format -show_streams -of json -- $Path
  if ($LASTEXITCODE -ne 0) {
    throw "ffprobe failed for $Path"
  }
  $probePath = Join-Path $probeDir "$ClipId.json"
  $json | Set-Content -LiteralPath $probePath -Encoding UTF8
  return ($json -join [Environment]::NewLine) | ConvertFrom-Json
}

function New-NormalClip {
  param(
    [Parameter(Mandatory = $true)][object]$Definition,
    [Parameter(Mandatory = $true)][string]$Destination,
    [string]$AudioPath,
    [string[]]$TestCard
  )

  if ((Test-Path -LiteralPath $Destination) -and -not $Force) {
    Write-Host "[skip] $(Split-Path $Destination -Leaf)"
    return
  }

  $source = $sourceByKey[$Definition.sourceKey]
  $sourcePath = Join-Path $sourceRoot $source.fileName
  $duration = 6.0
  if ($AudioPath) {
    $duration = [Math]::Max(4.0, (Get-AudioDurationSeconds -Path $AudioPath) + 0.6)
  }

  $cropX = if ($Definition.cropAnchor -eq 'right') { 'iw-1080' } elseif ($Definition.cropAnchor -eq 'left') { '0' } else { '(iw-1080)/2' }
  $videoFilter = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:${cropX}:0,fps=30"
  if ($TestCard -and $TestCard.Count -eq 2) {
    $line1 = $TestCard[0].Replace("'", "\\'").Replace(':', '\:')
    $line2 = $TestCard[1].Replace("'", "\\'").Replace(':', '\:')
    $videoFilter += ",drawbox=x=60:y=1380:w=960:h=340:color=black@0.78:t=fill"
    $videoFilter += ",drawtext=fontfile='$fontPath':text='$line1':fontcolor=white:fontsize=58:x=(w-text_w)/2:y=1435"
    $videoFilter += ",drawtext=fontfile='$fontPath':text='$line2':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=1535"
  }

  $args = @(
    '-hide_banner', '-loglevel', 'error',
    '-ss', ([string]::Format([Globalization.CultureInfo]::InvariantCulture, '{0:0.###}', [double]$Definition.startSeconds)),
    '-i', $sourcePath
  )
  if ($AudioPath) {
    $args += @('-i', $AudioPath)
  }
  $args += @('-vf', $videoFilter, '-map', '0:v:0')
  if ($AudioPath) {
    $args += @('-map', '1:a:0', '-af', 'apad=pad_dur=0.6', '-c:a', 'aac', '-ar', '48000', '-b:a', '192k')
  }
  else {
    $args += '-an'
  }
  $args += @(
    '-t', ([string]::Format([Globalization.CultureInfo]::InvariantCulture, '{0:0.###}', $duration)),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '20',
    '-movflags', '+faststart', '-y', $Destination
  )
  Invoke-Ffmpeg -Arguments $args
}

function Convert-ProbeToManifestFields {
  param([Parameter(Mandatory = $true)][object]$Probe)
  $video = $Probe.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1
  $audio = $Probe.streams | Where-Object { $_.codec_type -eq 'audio' } | Select-Object -First 1
  return @{
    durationMs = [int][Math]::Round(([double]$Probe.format.duration) * 1000)
    width = [int]$video.width
    height = [int]$video.height
    frameRate = $video.r_frame_rate
    videoCodec = $video.codec_name
    audioCodec = if ($audio) { $audio.codec_name } else { $null }
    audioSampleRate = if ($audio) { [int]$audio.sample_rate } else { $null }
  }
}

foreach ($clip in $plan.mainClips) {
  $wavPath = Join-Path $wavDir "$($clip.clipId).wav"
  if (-not (Test-Path -LiteralPath $wavPath)) {
    throw "TTS WAV is missing: $wavPath"
  }
  $destination = Join-Path $mainDir "$($clip.clipId).mp4"
  New-NormalClip -Definition $clip -Destination $destination -AudioPath $wavPath -TestCard @($clip.testCard)
}

$silentDefinition = [pscustomobject]@{ sourceKey = 'pov'; startSeconds = 0.5 }
New-NormalClip -Definition $silentDefinition -Destination (Join-Path $edgeDir 'wc-edge-01-silent.mp4')

$conflictDefinition = [pscustomobject]@{ sourceKey = 'interior'; startSeconds = 1.0 }
$rinseWav = Join-Path $wavDir 'wc-main-05-rinse.wav'
New-NormalClip -Definition $conflictDefinition -Destination (Join-Path $edgeDir 'wc-edge-02-av-conflict.mp4') -AudioPath $rinseWav

$lowVolumePath = Join-Path $edgeDir 'wc-edge-03-low-volume.mp4'
if ($Force -or -not (Test-Path -LiteralPath $lowVolumePath)) {
  $source = $sourceByKey['foam']
  $sourcePath = Join-Path $sourceRoot $source.fileName
  $voicePath = Join-Path $wavDir 'wc-main-01-hook.wav'
  $duration = [Math]::Max(4.0, (Get-AudioDurationSeconds -Path $voicePath) + 0.6)
  $args = @(
    '-hide_banner', '-loglevel', 'error', '-ss', '1.0', '-i', $sourcePath, '-i', $voicePath,
    '-f', 'lavfi', '-i', 'anoisesrc=color=pink:amplitude=0.004:sample_rate=48000',
    '-filter_complex', '[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[v];[1:a]volume=0.015,aresample=48000[voice];[2:a][voice]amix=inputs=2:duration=longest:weights=1 1[a]',
    '-map', '[v]', '-map', '[a]', '-t', ([string]::Format([Globalization.CultureInfo]::InvariantCulture, '{0:0.###}', $duration)),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '20',
    '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', '-y', $lowVolumePath
  )
  Invoke-Ffmpeg -Arguments $args
}

$duplicateSource = Join-Path $mainDir 'wc-main-04-foam.mp4'
foreach ($name in @('wc-edge-04-duplicate-a.mp4', 'wc-edge-04-duplicate-b.mp4')) {
  $destination = Join-Path $edgeDir $name
  if ($Force -or -not (Test-Path -LiteralPath $destination)) {
    Copy-Item -LiteralPath $duplicateSource -Destination $destination -Force
  }
}

$long = $plan.edgeLongSpeech
$longWav = Join-Path $wavDir "$($long.clipId).wav"
New-NormalClip -Definition $long -Destination (Join-Path $edgeDir "$($long.clipId).mp4") -AudioPath $longWav

$unsupportedPath = Join-Path $edgeDir 'wc-edge-06-unsupported.mp4'
if ($Force -or -not (Test-Path -LiteralPath $unsupportedPath)) {
  [IO.File]::WriteAllBytes($unsupportedPath, [byte[]](0x00, 0x00, 0x00, 0x18, 0x66, 0x74, 0x79, 0x70, 0x62, 0x72, 0x6f, 0x6b, 0x65, 0x6e))
}

$manifestClips = New-Object System.Collections.Generic.List[object]
foreach ($clip in $plan.mainClips) {
  $path = Join-Path $mainDir "$($clip.clipId).mp4"
  $probe = Get-MediaProbe -ClipId $clip.clipId -Path $path
  $fields = Convert-ProbeToManifestFields -Probe $probe
  $source = $sourceByKey[$clip.sourceKey]
  $transformations = @('trim', 'crop-9x16', 'replace-audio')
  if ($clip.testCard) { $transformations += 'test-data-card' }
  $manifestClips.Add([ordered]@{
    clipId = $clip.clipId
    fileName = "$($clip.clipId).mp4"
    set = 'main'
    expectedMarketingRole = $clip.expectedMarketingRole
    expectedVisualSummary = $clip.expectedVisualSummary
    ttsText = $clip.ttsText
    expectedAsrKeywords = @($clip.expectedAsrKeywords)
    audioMode = 'tts-replace'
    sourcePageUrl = $source.sourcePageUrl
    sourceDownloadUrl = ''
    sourceTitle = $source.sourceTitle
    sourceAuthor = $source.sourceAuthor
    licenseName = 'Pexels License'
    licenseUrl = 'https://www.pexels.com/license/'
    downloadedAt = '2026-08-12'
    licenseReviewedAt = '2026-09-01'
    sourceSha256 = $source.sourceSha256
    outputSha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    transformations = $transformations
    durationMs = $fields.durationMs
    width = $fields.width
    height = $fields.height
    frameRate = $fields.frameRate
    videoCodec = $fields.videoCodec
    audioCodec = $fields.audioCodec
    audioSampleRate = $fields.audioSampleRate
    containsFace = [bool]$source.containsFace
    containsPlate = [bool]$source.containsPlate
    containsTrademark = [bool]$source.containsTrademark
    testOnly = $true
    publishable = $false
  })
}

$edgeDefinitions = @(
  [ordered]@{ clipId='wc-edge-01-silent'; sourceKey='pov'; role='transition'; summary='车内视角观察挡风玻璃上的冲洗水流，但文件完全没有音轨'; tts=''; keywords=@(); audioMode='none'; transformations=@('trim','crop-9x16','remove-audio'); intentionallyMisleading=$false },
  [ordered]@{ clipId='wc-edge-02-av-conflict'; sourceKey='interior'; role='detail'; summary='画面为内饰吸尘，口播却故意描述高压水流冲洗车身'; tts='再用高压水流冲净泡沫，减少泥沙残留。'; keywords=@('高压水流','冲净泡沫'); audioMode='tts-conflict'; transformations=@('trim','crop-9x16','replace-audio'); intentionallyMisleading=$true },
  [ordered]@{ clipId='wc-edge-03-low-volume'; sourceKey='foam'; role='hook'; summary='洗车工位喷洒水雾画面，叠加极弱口播与轻微粉红噪声'; tts='你的车多久没有彻底洗过了？'; keywords=@('你的车','多久'); audioMode='tts-low-volume-with-noise'; transformations=@('trim','crop-9x16','low-volume','add-noise'); intentionallyMisleading=$false },
  [ordered]@{ clipId='wc-edge-04-duplicate-a'; sourceKey='wide-foam'; role='process'; summary='同一泡沫喷洗成品的第一份独立上传文件'; tts='先用泡沫软化车身表面的灰尘和污渍。'; keywords=@('泡沫','软化'); audioMode='tts-replace'; transformations=@('exact-copy-of-main-04'); intentionallyMisleading=$false },
  [ordered]@{ clipId='wc-edge-04-duplicate-b'; sourceKey='wide-foam'; role='process'; summary='同一泡沫喷洗成品的第二份独立上传文件'; tts='先用泡沫软化车身表面的灰尘和污渍。'; keywords=@('泡沫','软化'); audioMode='tts-replace'; transformations=@('exact-copy-of-main-04'); intentionallyMisleading=$false },
  [ordered]@{ clipId='wc-edge-05-long-speech'; sourceKey='wide-foam'; role='process'; summary='横版车身泡沫覆盖画面，配有包含两个短句的连续长口播'; tts=$long.ttsText; keywords=@($long.expectedAsrKeywords); audioMode='tts-replace'; transformations=@('trim','crop-9x16','replace-audio'); intentionallyMisleading=$false }
)

foreach ($edge in $edgeDefinitions) {
  $path = Join-Path $edgeDir "$($edge.clipId).mp4"
  $probe = Get-MediaProbe -ClipId $edge.clipId -Path $path
  $fields = Convert-ProbeToManifestFields -Probe $probe
  $source = $sourceByKey[$edge.sourceKey]
  $manifestClips.Add([ordered]@{
    clipId = $edge.clipId
    fileName = "$($edge.clipId).mp4"
    set = 'edge'
    expectedMarketingRole = $edge.role
    expectedVisualSummary = $edge.summary
    ttsText = $edge.tts
    expectedAsrKeywords = @($edge.keywords)
    audioMode = $edge.audioMode
    intentionallyMisleading = [bool]$edge.intentionallyMisleading
    sourcePageUrl = $source.sourcePageUrl
    sourceDownloadUrl = ''
    sourceTitle = $source.sourceTitle
    sourceAuthor = $source.sourceAuthor
    licenseName = 'Pexels License'
    licenseUrl = 'https://www.pexels.com/license/'
    downloadedAt = '2026-08-12'
    licenseReviewedAt = '2026-09-01'
    sourceSha256 = $source.sourceSha256
    outputSha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    transformations = @($edge.transformations)
    durationMs = $fields.durationMs
    width = $fields.width
    height = $fields.height
    frameRate = $fields.frameRate
    videoCodec = $fields.videoCodec
    audioCodec = $fields.audioCodec
    audioSampleRate = $fields.audioSampleRate
    containsFace = [bool]$source.containsFace
    containsPlate = [bool]$source.containsPlate
    containsTrademark = [bool]$source.containsTrademark
    testOnly = $true
    publishable = $false
  })
}

$unsupportedHash = (Get-FileHash -LiteralPath $unsupportedPath -Algorithm SHA256).Hash
$manifestClips.Add([ordered]@{
  clipId = 'wc-edge-06-unsupported'
  fileName = 'wc-edge-06-unsupported.mp4'
  set = 'edge'
  expectedMarketingRole = $null
  expectedVisualSummary = '故意损坏且不可解码的隔离上传文件'
  ttsText = ''
  expectedAsrKeywords = @()
  audioMode = 'invalid-container'
  intentionallyMisleading = $false
  sourcePageUrl = ''
  sourceDownloadUrl = ''
  sourceTitle = 'Locally generated invalid container fixture'
  sourceAuthor = 'Test package generator'
  licenseName = 'Locally generated test fixture'
  licenseUrl = ''
  downloadedAt = ''
  licenseReviewedAt = '2026-09-01'
  sourceSha256 = ''
  outputSha256 = $unsupportedHash
  transformations = @('write-invalid-ftyp-fixture')
  durationMs = 0
  width = 0
  height = 0
  frameRate = ''
  videoCodec = ''
  audioCodec = $null
  audioSampleRate = $null
  containsFace = $false
  containsPlate = $false
  containsTrademark = $false
  testOnly = $true
  publishable = $false
})

$manifest = [ordered]@{
  schemaVersion = $plan.schemaVersion
  packageVersion = $plan.packageVersion
  createdAt = $plan.createdAt
  testOnly = $true
  publishable = $false
  voice = [ordered]@{
    apiVoiceId = $plan.voice
    authorizationStatus = 'not-confirmed-for-public-commercial-use'
    usage = 'local-internal-test-only'
  }
  rightsReview = [ordered]@{
    reviewedAt = '2026-09-01'
    pexelsLicenseUrl = 'https://www.pexels.com/license/'
    pexelsTermsUrl = 'https://www.pexels.com/terms-of-service/'
    sourceDownloadUrlsRecovered = $false
    thirdPartyRightsFullyCleared = $false
    notes = 'Pexels source pages and current license were reviewed. Public use remains disabled because identifiable people, vehicle/product marks, property context, direct download URLs, and the bundled TTS voice authorization were not fully cleared.'
  }
  clips = $manifestClips
}

$manifestPath = Join-Path $packageRoot 'manifests\assets.json'
$manifest | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
Write-Host "Package build complete: $packageRoot"
