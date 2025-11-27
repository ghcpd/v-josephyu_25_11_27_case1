# PowerShell setup script
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Write-Host "Virtual environment created and dependencies installed. Activate with: .\\.venv\\Scripts\\Activate.ps1"