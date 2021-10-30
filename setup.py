from setuptools import setup

## Config
MAJOR = 0
MINOR = 3
PATCH = 2
with open("README.rst", "r", encoding="utf-8", errors="ignore") as readme:
    LONG_DESCRIPTION = readme.read()

## Setuptools config
paramaters = dict(
    name = "mail_to_sms",
    packages = ["mail_to_sms"],
    package_data = {
        "": [
            "gateways.json",
        ],
    },
    version = "{0}.{1}.{2}".format(MAJOR, MINOR, PATCH),
    description = "Programmatically send out text messages via email.",
    long_description = LONG_DESCRIPTION,
    author = "Nick Schorr",
    author_email = "naschorr@gmail.com",
    url = "https://github.com/naschorr/mail-to-sms",
    install_requires = [
        "keyring >= 10.4",
        "yagmail >= 0.6",
        "phonenumbers >= 8.4 ",
        "click >= 6.7",
    ],
    entry_points = {
        "console_scripts": [
            "mail_to_sms = mail_to_sms.mail_to_sms_cli:main",
        ],
    },
    ## Todo: Add test_suite to the setup
    license = "MIT License",
    keywords = ["sms", "mms", "messaging", "mail", "api"],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
)

## Run the setup
setup(**paramaters)
