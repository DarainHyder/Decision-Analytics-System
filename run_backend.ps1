Set-Location $PSScriptRoot
.\backend\venv\Scripts\activate
$env:PYTHONPATH = $PSScriptRoot
uvicorn backend.main:app --reload
