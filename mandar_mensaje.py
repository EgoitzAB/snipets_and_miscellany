#!/usr/bin/python3

from twilio.rest import Client

account_sid = 'ACd583b9d8d4b1f740c2f72c3455c412be'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+15074193658',
  body='Hola, este es un mensaje de prueba',
  to='+34662459847'
)

print(message.sid)