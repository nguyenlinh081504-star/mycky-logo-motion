param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ToolArgs)
$ErrorActionPreference='Stop'
$skillDirectory=Split-Path -Parent $PSScriptRoot
$configFile=Join-Path $skillDirectory 'runtime.local.json'
$settings=if(Test-Path -LiteralPath $configFile){Get-Content -LiteralPath $configFile -Raw | ConvertFrom-Json}else{$null}
$pythonPath=$null
if($env:MYCKY_PYTHON){$pythonPath=$env:MYCKY_PYTHON}
elseif($settings -and $settings.python){$pythonPath=$settings.python}
else{
  foreach($candidateName in @('python','python3','py')){
    $candidateCommand=Get-Command $candidateName -ErrorAction SilentlyContinue
    if($candidateCommand){$pythonPath=$candidateCommand.Source;break}
  }
}
if(-not $pythonPath){throw 'Không tìm thấy Python có sẵn. Đặt MYCKY_PYTHON hoặc cấu hình runtime.local.json từ runtime.example.json.'}
$env:PYTHONUTF8='1'
& $pythonPath (Join-Path $PSScriptRoot 'logo_lab.py') @ToolArgs
exit $LASTEXITCODE
