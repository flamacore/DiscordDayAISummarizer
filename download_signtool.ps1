# PowerShell script to download signtool.exe if not available
# This script downloads a standalone version of signtool.exe

$toolsDir = Join-Path $PSScriptRoot "tools"
$signtoolPath = Join-Path $toolsDir "signtool.exe"

# Create tools directory if it doesn't exist
if (!(Test-Path $toolsDir)) {
    New-Item -ItemType Directory -Path $toolsDir -Force | Out-Null
}

# Check if signtool already exists
if (Test-Path $signtoolPath) {
    Write-Host "✅ signtool.exe already exists at $signtoolPath"
    exit 0
}

Write-Host "📥 Downloading signtool.exe..."

try {
    # URL for a standalone signtool.exe (this is a hypothetical URL - in practice you'd need a real source)
    # For now, we'll just create a placeholder and suggest manual download
    
    Write-Host "⚠️ signtool.exe needs to be downloaded manually."
    Write-Host "Please download Windows SDK from:"
    Write-Host "https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/"
    Write-Host ""
    Write-Host "Or extract signtool.exe from the SDK and place it in: $signtoolPath"
    Write-Host ""
    Write-Host "Alternative: Install Visual Studio with Windows SDK components"
    
    exit 1
} catch {
    Write-Host "❌ Failed to download signtool.exe: $_"
    exit 1
}
