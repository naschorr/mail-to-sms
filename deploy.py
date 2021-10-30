import click
import sys
import os
import re
import pypandoc as pandoc
import glob

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


def generate_readme_rst() -> bool:
    '''Converts the REAME.md to a .rst file for pypi'''

    try:
        pandoc.convert_file("README.md", "rst", outputfile="README.rst", extra_args=["--verbose"])
    except OSError as e:
        if("no pandoc was found" in str(e).lower() or True):
            print("Pandoc wasn't found, attempting to install...")

            from pypandoc.pandoc_download import download_pandoc
            download_pandoc()

            print("Pandoc was installed, attempting to generate README.rst again...")
            generate_readme_rst()

            print("Cleaning up installer...")
            try:
                pandoc_installers = glob.glob("pandoc-*", recursive=False)
                for installer in pandoc_installers:
                    os.remove(installer)
            except:
                print(f"Unable to automatically clean up pandoc installer{'s' if (len(pandoc_installers) != 0) else ''}: {pandoc_installers}.")

    except:
        print("An unknown error occured while attempting to generate README.rst")
        return False

    return True


@click.command()
@click.option("--pypi", is_flag=True, help="Deploy to the pypi repo in your ~/.pyirc file, rather than testpypi")
@click.option("--no-deploy", "-d", is_flag=True, help="Don't actually deploy to pypi, but do everything else.")
def deploy(pypi, no_deploy):
    version = get_version()
    print("Building {0}, pypi={1}, no_deploy={2}\n".format(version, pypi, no_deploy))

    ## Run tests before anything else happens, and make sure they're passing
    print("Running tests before continuing deployment...")
    if (not tests.test_runner.main()):
        print("Tests failed, quitting.")
        return
    print("Tests passed\n")

    ## Build the README.rst
    print("Converting README.md to a .rst for PyPI")
    if (not generate_readme_rst()):
        print("Unable to generate README.rs")
        return
    print("README.rst was generated\n")

    # import setup

    ## Build the wheel
    if(pypi):
        print("Building wheel for PyPI")
        setup_retval = os.system(f"\"\"{sys.executable}\" setup.py register sdist bdist_wheel\"")
    else:
        print("Building wheel for test PyPI")
        setup_retval = os.system(f"\"\"{sys.executable}\" setup.py register -r testpypi sdist bdist_wheel\"")
    assert setup_retval == 0
    print("Wheel built\n")

    ## Deploy the wheel to the chosen repo!
    if(not no_deploy):
        if(pypi):
            print("Deploying to PyPI")
            deploy_retval = os.system("twine upload dist/mail_to_sms-{0}*".format(version))
        else:
            print("Deploying to test PyPI")
            deploy_retval = os.system("twine upload dist/mail_to_sms-{0}* -r testpypi".format(version))
        assert deploy_retval == 0
        print("Deployment complete\n")

    ## Cleanup
    print("Performing final cleanup\n")
    os.remove("README.rst")

    print("Done!")


if(__name__ == "__main__") :
    deploy()