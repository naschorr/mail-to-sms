from distutils.core import setup

setup(
	name = "mail_to_sms",
	packages = ["mail_to_sms"],
    package_data = {
        '': ["gateways.json"],
    },
	version = "0.1.0",
	description = "Programmatically send out text messages via email.",
	author = "Nick Schorr",
	author_email = "naschorr@gmail.com",
	url = "https://github.com/naschorr/mail-to-sms",
	download_url = "https://github.com/naschorr/mail-to-sms/archive/0.1.0.tar.gz",
	install_requires = [
		"yagmail",
		"phonenumbers",
	],
	keywords = ["sms", "mms", "messaging", "mail"],
	classifiers = [
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Programming Language :: Python :: 3"
	],
)