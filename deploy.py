from __future__ import print_function

## Inspired by https://github.com/kootenpv/yagmail/blob/master/deploy.py

import click
import sys
import os
import re
import pypandoc as pandoc


## Get current program version from setup.py
def get_version():
    with open("setup.py") as fd:
        setup = fd.read()

    try:
        major = re.search(r"MAJOR ?= ?([0-9]+)", setup).group(1)
        minor = re.search(r"MINOR ?= ?([0-9]+)", setup).group(1)
        patch = re.search(r"PATCH ?= ?([0-9]+)", setup).group(1)
    except:
        print("Invalid version found, quitting.")
        return None
    else:
        return "{0}.{1}.{2}".format(major, minor, patch)


## Converts the REAME.md to a .rst file for pypi
def readme_to_rst():
    ## Assumes pypandoc has installed pandoc. If not, use:
    ## from pypandoc.pandoc_download import download_pandoc
    ## download_pandoc()
    pandoc.convert_file("README.md", "rst", outputfile="README.rst")


@click.command()
@click.option("--pypi", is_flag=True, help="Deploy to the pypi repo in your ~/.pyirc file, rather than testpypi")
def deploy(pypi):
    version = get_version()
    print("Building {0}, pypi={1}".format(version, pypi))
    sys.stdout.flush()

    ## Build the README.rst
    readme_to_rst()

    ## Assumes that python points to the correct python installation, and that
    ## twine is installed and accessible from the command line.
    retval = os.system("python setup.py register sdist bdist_wheel")
    assert retval == 0

    ## Deploy to chosen repo
    if(pypi):
        retval = os.system("twine upload dist/mail_to_sms-{0}*".format(version))
    else:
        retval = os.system("twine upload dist/mail_to_sms-{0}* -r testpypi".format(version))
    assert retval == 0

    ## Cleanup
    os.remove("README.rst")


if(__name__ == "__main__") :
    deploy()