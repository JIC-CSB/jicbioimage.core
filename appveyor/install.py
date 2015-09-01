import os, os.path
import zipfile

try: 
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


def downlad_file(url, fname):
    """Download file from url and save as fname."""
    print("Downloading {} as {}".format(url, fname))
    response = urlopen(url)
    download = response.read()
    with open(fname, 'wb') as fh:
        fh.write(download)


def unzip_file(zip_fname):
    """Unzip the zip_fname in the current directory.""" 
    print("Unzipping {}".format(zip_fname))
    with zipfile.ZipFile(zip_fname) as zf:
        zf.extractall()

def install_from_zip(url):
    """Download and unzip from url."""
    fname = 'tmp.zip'
    downlad_file(url, fname)
    unzip_file(fname)
    print("Removing {}".format(fname))
    os.unlink(fname)

def install_bftools():
    print("Installing bftools.")
#   url = 'http://downloads.openmicroscopy.org/latest/bio-formats5.1/artifacts/bftools.zip'
# Using older version of bftools as 5.1 appears to depend on SlideBook6Reader.dll
    url = 'http://downloads.openmicroscopy.org/bio-formats/5.0.8/artifacts/bftools.zip'
    install_from_zip(url)

def install_freeimage():
    print("Installing freeimage.")
    url = 'http://downloads.sourceforge.net/freeimage/FreeImage3170Win32Win64.zip'
    install_from_zip(url)

def main():
    print("Running {}.{}".format(__file__, __name__))
    os.chdir("/")
    print("Working directory: {}".format(os.getcwd()))
    install_bftools()
    install_freeimage()

main()
