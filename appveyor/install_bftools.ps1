# Script to install bftools under Windows.

$BFTOOLS_URL = "http://downloads.openmicroscopy.org/latest/bio-formats5.1/artifacts/bftools.zip"
$BFTOOLS_ZIP_PATH = "C:\bftools.zip"
$BFTOOLS_DIR = "C:\bftools"
$BFCONVERT_PATH = "C:\bftools\bfconvert.bat"

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
    } else {
        Write-Host "bftools already installed."
    }
}

function main () {
    InstallBFTools
}

main
