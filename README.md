# mail-to-sms 
Programmatically send out text messages via email.

[![PyPI version](https://badge.fury.io/py/mail_to_sms.svg)](https://badge.fury.io/py/mail_to_sms)

### Installation
`pip install mail_to_sms` and import like any other Python module. Or,

`git clone https://github.com/naschorr/mail-to-sms` locally as needed. Make sure to install the requirements with `pip install -r requirements.txt`

### Arguments
- **number** {*string|int*}: The destination phone number (ex. `5551234567`).
- **carrier** {*string*}: The destination phone number's carrier (ex. `"att"`). Current carriers include: `"alltel"`, `"at&t"`, `"att"`, `"boost mobile"`, `"boost"`, `"cricket wireless"`, `"cricket"`, `"metropcs"`, `"project fi"`, `"fi"`, `"sprint"`, `"t-mobile"`, `"t mobile"`, `"tmobile"`, `"us cellular"`, `"verizon wireless"`, `"verizon"`, `"vzw"`, `"virgin mobile"`, and `"virgin"`.
- **username** {*string*} [optional]: The username for accessing the SMTP server (ex. `"username"`). If omitted, it'll try to use the username stored in the [.yagmail file](https://github.com/kootenpv/yagmail#username-and-password).
- **password** {*string*} [optional]: The password for accessing the SMTP server (ex. `"password"`). If using Gmail and 2FA, you may want to use an app password. If omitted, it'll try to use [yagmail's password](https://github.com/kootenpv/yagmail#username-and-password) in the keyring, otherwise it'll prompt you for the password.
- **contents** {[*yagmail contents*](https://github.com/kootenpv/yagmail#magical-contents)} [optional]: A yagmail friendly contents argument (ex. `"This is a message."`). If omitted, MailToSMS's `send()` method can be called manually.
- keyworded args (for extra configuration):
  - **quiet** {*boolean*}: Choose to disable printed statements. Defaults to False. (ex. `quiet=True`)
  - **region** {*string*}: The region of the destination phone number. Defaults to "US". (ex. `region="US"`). This should only be necessary when using a non international phone number that's not US based. See the phonenumbers repo [here](https://github.com/daviddrysdale/python-phonenumbers).
  - **mms** {*boolean*}: Choose to send a MMS message instead of a SMS message, but will fallback to SMS if MMS isn't present. Defaults to False. (ex. `mms=True`)
  - **subject** {*string*}: The subject of the email to send (ex. `subject="This is a subject."`)
  - **yagmail** {*list*}: A list of arguments to send to the yagmail.SMTP() constructor. (ex. `yagmail=["my.smtp.server.com", "12345"]`). As of 4/30/17, the args and their defaults (after the username and password) are `host='smtp.gmail.com'`, `port='587'`, `smtp_starttls=True`, `smtp_set_debuglevel=0`, `smtp_skip_login=False`, `encoding="utf-8"`. This is unnecessary if you're planning on using the basic Gmail interface, in which case you'll just need the username and password. This may make more sense if you look at yagmail's SMTP class [here](https://github.com/kootenpv/yagmail/blob/master/yagmail/yagmail.py#L49).

### Examples
```
from mail_to_sms import MailToSMS
```

```
MailToSMS(5551234567, "att", "username@gmail.com", "password", "this is a message")
```

```
MailToSMS("5551234567", "att", "username", "password", ["hello", "world"], subject="hey!")
```

```
MailToSMS(5551234567, "att", "username", "password", "hello world!", yagmail=["smtp.gmail.com", "587"])
```

```
MailToSMS("5551234567", "att", "username@gmail.com", "password", ["line one"], yagmail=["smtp.gmail.com"])
```

```
mail = MailToSMS(5551234567, "att", "username", "password")
mail.send("this is a string!")
```

### CLI Examples
Note that you may want to install `mail_to_sms` into your global python's site-packages rather than just a virtualenv if you're planning on using the CLI.
```
> mail_to_sms 5551234567 att "just a test"
```

```
> mail_to_sms 5551234567 "att" "hey, world!" -u "username"
```

```
> mail_to_sms "5551234567" att "nice job" -u "username" -p "password"
```

### Requirements
- [keyring](https://github.com/jaraco/keyring)
- [yagmail](https://github.com/kootenpv/yagmail)
- [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers)
- [click](https://github.com/pallets/click) (for the CLI)

### Note
I've only been able to test this on AT&T and Verizon, so I can't guarantee that this works for other carriers. Feedback is appreciated.
