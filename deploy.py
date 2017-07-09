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
def generate_readme_rst(attempts=0):
    ## Assumes pypandoc has installed pandoc. If not, use:
    ## from pypandoc.pandoc_download import download_pandoc
    ## download_pandoc()
    pandoc.convert_file("README.md", "rst", outputfile="README.rst")


@click.command()
@click.option("--pypi", is_flag=True, help="Deploy to the pypi repo in your ~/.pyirc file, rather than testpypi")
@click.option("--no-deploy", "-d", is_flag=True, help="Don't actually deploy to pypi, but do everything else.")
def deploy(pypi, no_deploy):
    version = get_version()
    print("Building {0}, pypi={1}, no_deploy={2}".format(version, pypi, no_deploy))
    sys.stdout.flush()

    ## Build the README.rst
    generate_readme_rst()

    ## Assumes that python points to the correct python installation, and that
    ## twine is installed and accessible from the command line.
    if(pypi):
        setup_retval = os.system("python setup.py register sdist bdist_wheel")
    else:
        setup_retval = os.system("python setup.py register -r testpypi sdist bdist_wheel")
    assert setup_retval == 0

    if(not no_deploy):
        ## Deploy to chosen repo
        if(pypi):
            deploy_retval = os.system("twine upload dist/mail_to_sms-{0}*".format(version))
        else:
            deploy_retval = os.system("twine upload dist/mail_to_sms-{0}* -r testpypi".format(version))
        assert deploy_retval == 0

    ## Cleanup
    os.remove("README.rst")


if(__name__ == "__main__") :
    deploy()