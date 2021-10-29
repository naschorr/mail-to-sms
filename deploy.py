import click
import sys
import os
import re
import pypandoc as pandoc

import tests.test_runner

## Inspired by https://github.com/kootenpv/yagmail/blob/master/deploy.py

def get_version():
    '''Get current program version from setup.py'''
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


def generate_readme_rst():
    '''Converts the REAME.md to a .rst file for pypi'''

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

    ## Run tests before anything else happens, and make sure they're passing
    print("Running tests before continuing deployment...")
    if (not tests.test_runner.main()):
        print("Tests failed, quitting.")
    print("Tests passed.")

    ## Build the README.rst
    print("Converting README.md to a .rst for PyPI")
    generate_readme_rst()

    ## Assumes that python points to the correct python installation, and that
    ## twine is installed and accessible from the command line.
    if(pypi):
        print("Building wheel for PyPI")
        setup_retval = os.system("python setup.py register sdist bdist_wheel")
    else:
        print("Building wheel for test PyPI")
        setup_retval = os.system("python setup.py register -r testpypi sdist bdist_wheel")
    assert setup_retval == 0

    if(not no_deploy):
        ## Deploy to chosen repo
        if(pypi):
            print("Deploying to PyPI")
            deploy_retval = os.system("twine upload dist/mail_to_sms-{0}*".format(version))
        else:
            print("Deploying to test PyPI")
            deploy_retval = os.system("twine upload dist/mail_to_sms-{0}* -r testpypi".format(version))
        assert deploy_retval == 0

    ## Cleanup
    print("Performing final cleanup.")
    os.remove("README.rst")

    print("Done!")


if(__name__ == "__main__") :
    deploy()