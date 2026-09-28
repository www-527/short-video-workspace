param(
  [string]$ApiBaseUrl = 'http://127.0.0.1:9010',
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$planPath = Join-Path $packageRoot 'manifests\package-plan.json'
$wavDir = Join-Path $packageRoot 'tts\wav'
$responseDir = Join-Path $packageRoot 'reports\tts-responses'
$plan = Get-Content -LiteralPath $planPath -Raw -Encoding UTF8 | ConvertFrom-Json

New-Item -ItemType Directory -Path $wavDir, $responseDir -Force | Out-Null

function Invoke-JsonRequest {
  param(
    [Parameter(Mandatory = $true)][string]$Uri,
    [Parameter(Mandatory = $true)][object]$Body
  )

  $json = $Body | ConvertTo-Json -Depth 10 -Compress
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
  try {
    return Invoke-RestMethod -Method Post -Uri $Uri -ContentType 'application/json; charset=utf-8' -Body $bytes -TimeoutSec 1200
  }
  catch {
    $status = $null
    if ($_.Exception.Response) {
      $status = [int]$_.Exception.Response.StatusCode
    }
    $details = $_.ErrorDetails.Message
    throw "IndexTTS2 request failed. httpStatus=$status; message=$($_.Exception.Message); response=$details"
  }
}

function Invoke-GetUtf8Json {
  param([Parameter(Mandatory = $true)][string]$Uri)

  $client = New-Object System.Net.WebClient
  try {
    $bytes = $client.DownloadData($Uri)
    $json = [System.Text.Encoding]::UTF8.GetString($bytes)
    return $json | ConvertFrom-Json
  }
  finally {
    $client.Dispose()
  }
}

$health = Invoke-GetUtf8Json -Uri "$ApiBaseUrl/api/health"
if (-not $health.ok) {
  throw "IndexTTS2 health check returned ok=false: $($health | ConvertTo-Json -Depth 10 -Compress)"
}

$voices = Invoke-GetUtf8Json -Uri "$ApiBaseUrl/api/voices"
if ($plan.voice -notin @($voices.voices | ForEach-Object { $_.name })) {
  throw "Configured voice is not present in /api/voices: $($plan.voice)"
}

$requests = @($plan.mainClips) + @($plan.edgeLongSpeech)
foreach ($item in $requests) {
  $target = Join-Path $wavDir "$($item.clipId).wav"
  if ((Test-Path -LiteralPath $target) -and -not $Force) {
    Write-Host "[skip] $($item.clipId)"
    continue
  }

  Write-Host "[tts] $($item.clipId): $($item.ttsText)"
  $payload = @{
    text = $item.ttsText
    voice = $plan.voice
    speed = 1.0
    emotion = @{
      mode = 'text'
      text = '真诚、清晰、自然、有一点活力的洗车服务口播'
      weight = 0.5
    }
  }

  $result = Invoke-JsonRequest -Uri "$ApiBaseUrl/api/tts" -Body $payload
  $responsePath = Join-Path $responseDir "$($item.clipId).json"
  $result | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $responsePath -Encoding UTF8
  if (-not $result.ok -or -not $result.audioPath -or -not (Test-Path -LiteralPath $result.audioPath)) {
    throw "IndexTTS2 returned an unusable result for $($item.clipId): $($result | ConvertTo-Json -Depth 10 -Compress)"
  }

  Copy-Item -LiteralPath $result.audioPath -Destination $target -Force
}

Write-Host "TTS generation complete: $wavDir"
