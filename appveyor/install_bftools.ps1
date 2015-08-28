# Script to install bftools under Windows.

$BFTOOLS_URL = "http://downloads.openmicroscopy.org/latest/bio-formats5.1/artifacts/bftools.zip"
$BFTOOLS_ZIP_PATH = "C:\bftools.zip"
$BFTOOLS_DIR = "C:\bftools"
$BFCONVERT_PATH = "C:\bftools\bfconvert.bat"

$FREEIMAGE_URL = "http://downloads.sourceforge.net/freeimage/FreeImage3170Win32Win64.zip"
$FREEIMAGE_ZIP_PATH = "C:\FreeImage3170Win32Win64.zip"
$FREEIMAGE_PATH = "$env:MINICONDA\envs\test-environment\lib"

function Expand-ZIPFile($file, $destination) {
    if(!(Test-Path -Path $destination )){
        New-Item -ItemType directory -Path $destination
    }
    $shell = New-Object -ComObject Shell.Application
    $zip = $shell.NameSpace($file)
    foreach($item in $zip.items()) {
        $shell.Namespace($destination).copyhere($item)
    }
}
 
function InstallBFTools () {
    if (-not(Test-Path $BFCONVERT_PATH)) {
        Write-Host "Installing bftools..."
        $webclient = New-Object System.Net.WebClient
        $webclient.DownloadFile($BFTOOLS_URL, $BFTOOLS_ZIP_PATH)
        Expand-ZIPFile -File $BFTOOLS_ZIP_PATH -Destination $BFTOOLS_DIR
        Write-Host "ls $BFTOOLS_DIR"
        Write-Host ls $BFTOOLS_DIR
    } else {
        Write-Host "bftools already installed."
    }
}

function InstallFreeImage () {
    Write-Host "Installing freeimage..."
    $webclient = New-Object System.Net.WebClient
    $webclient.DownloadFile($FREEIMAGE_URL, $FREEIMAGE_ZIP_PATH)
    Expand-ZIPFile -File $FREEIMAGE_ZIP_PATH -Destination $FREEIMAGE_PATH
    Write-Host "ls $FREEIMAGE_PATH"
    Write-Host ls $FREEIMAGE_PATH
}

function main () {
    InstallBFTools
    InstallFreeImage
}

main
