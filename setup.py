from distutils.core import setup

setup(
	name = "mail_to_sms",
	packages = ["mail_to_sms"],
    package_data = {
        '': [
        	"gateways.json",
        	"LICENSE.txt"
        ],
    },
	version = "0.2.0",
	description = "Programmatically send out text messages via email.",
	author = "Nick Schorr",
	author_email = "naschorr@gmail.com",
	url = "https://github.com/naschorr/mail-to-sms",
	download_url = "https://github.com/naschorr/mail-to-sms/archive/0.2.0.tar.gz",
	install_requires = [
		"yagmail",
		"phonenumbers",
	],
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
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5"
	],
)