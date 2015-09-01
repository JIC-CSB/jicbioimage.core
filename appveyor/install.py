import os, os.path
import urllib2
import zipfile


def downlad_file(url, fname):
    """Download file from url and save as fname."""
    response = urllib2.urlopen(url)
    download = response.read()
    with open(fname, 'wb') as fh:
        fh.write(download)


def unzip_file(zip_fname):
    """Unzip the zip_fname in the current directory.""" 
    with zipfile.ZipFile(zip_fname) as zf:
        zf.extractall()

def install_from_zip(url):
    """Download and unzip from url."""
    fname = 'tmp.zip'
    downlad_file(url, fname)
    unzip_file(fname)
    os.unlink(fname)

def install_bftools():
    url = 'http://downloads.openmicroscopy.org/latest/bio-formats5.1/artifacts/bftools.zip'
    install_from_zip(url)

def install_freeimage():
    url = 'http://downloads.sourceforge.net/freeimage/FreeImage3170Win32Win64.zip'
    install_from_zip(url)

def main():
    install_bftools()
    install_freeimage()

main()
