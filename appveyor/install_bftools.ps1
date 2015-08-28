$BFTOOLS_URL = "http://downloads.openmicroscopy.org/latest/bio-formats5.1/artifacts/bftools.zip"
$BFTOOLS_ZIP_PATH = "C:\bftools.zip"
$BFCONVERT_PATH = "C:\bftools\bfconvert.bat"

if (-not(Test-Path $BFCONVERT_PATH)) {
    Write-Host "Installing bftools..."
    $webclient = New-Object System.Net.WebClient
    $webclient.DownloadFile($BFTOOLS_URL $BFTOOL_ZIP_PATH)
    Write-Host "Executing:" unzip $BFTOOLS_ZIP_PATH
    Start-Process unzip -ArgumentList "$BFTOOLS_ZIP_PATH" -Wait -Passthru
} else {
    Write-Host "bftools already installed."
}
