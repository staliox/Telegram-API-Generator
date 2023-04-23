# Telegram API Hash Generator

An app for create or get telegram api id and api

## Possibilities
  - Fast response to messages and communication with the Telegram
  - Simple and Comprehensive

## Example
``` python
from tgapi import TelegramApplication

app = TelegramApplication(PHONE_NUMBER)
send_password = app.send_password()

if send_password:
    auth_login = app.auth_login(PASSWORD)
    
    if auth_login:
        auth_app = app.auth_app()
        print(auth_app)
```
