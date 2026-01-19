Set-Location "$PSScriptRoot\backend"
Write-Host "Creating Python virtual environment..."
python -m venv venv
Write-Host "Activating venv and installing dependencies..."
.\venv\Scripts\activate
pip install -r requirements.txt
Write-Host "Backend setup complete!"
