# mail-to-sms
Programmatically send out text messages via email.

### Requirements
- yagmail
- phonenumbers

Install with `pip install -r requirements.txt`

### Arguments
- **number** {*string|int*}: The destination phone number (ex. `5551234567`).
- **carrier** {*string*}: The destination phone number's carrier (ex. `"att"`).
- **username** {*string*}: The username for accessing the SMTP server (ex. `"username"`).
- **password** {*string*}: The password for accessing the SMTP server (ex. `"password"`). If using Gmail and 2FA, you may want to use an app password.
- **contents** {[*yagmail contents*](https://github.com/kootenpv/yagmail#magical-contents)}: A yagmail friendly contents argument (ex. `"This is a message."`).
- keyworded args (for extra configuration):
  - **region** {*string*}: The region of the destination phone number. Defaults to "US". (ex. `region="US"`). This should only be necessary when using a non international phone number that's not US based. See the phonenumbers repo [here](https://github.com/daviddrysdale/python-phonenumbers).
  - **mms** {*boolean*}: Choose to send a MMS message instead of a SMS message, but will fallback to SMS if MMS isn't present. Defaults to False. (ex. `mms=True`)
  - **subject** {*string*}: The subject of the email to send (ex. `subject="This is a subject."`)
  - **yagmail** {*list*}: A list of arguments to send to the yagmail.SMTP() constructor. (ex. `yagmail=["my.smtp.server.com", "12345"]`). As of 4/30/17, the args and their defaults (after the username and password) are `host='smtp.gmail.com'`, `port='587'`, `smtp_starttls=True`, `smtp_set_debuglevel=0`, `smtp_skip_login=False`, `encoding="utf-8"`. This is unnecessary if you're planning on using the basic Gmail interface, in which case you'll just need the username and password. This may make more sense if you look at yagmail's SMTP class [here](https://github.com/kootenpv/yagmail/blob/master/yagmail/yagmail.py#L49).

### Examples
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

### Note
I've only been able to test this on AT&T, so I can't guarantee that this works for other carriers. Feedback is appreciated.
