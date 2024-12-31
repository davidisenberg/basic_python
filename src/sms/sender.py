import os
from twilio.rest import Client
from sms.sms_api_key import get_account_sid, get_auth_token,get_phone_number

# Download the helper library from https://www.twilio.com/docs/python/install
# ? Shorthand identifier for your profile: My first Twilio account
# Created API Key ___ and stored the secret in Config. See: https://www.twilio.com/console/runtime/api-keys/_____
# twilio-cli configuration saved to "C:\Users\david\.twilio-cli\config.json"
# Saved My first Twilio account.
#  You don't have any active profile set, run "twilio profiles:use" to set a profile as active

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# https://www.twilio.com/blog/register-phone-number-send-sms-twilio-cli
# twilio profiles:use "My first Twilio account"
# twilio api:core:incoming-phone-numbers:create --phone-number="___"

account_sid = get_account_sid()
auth_token = get_auth_token()
client = Client(account_sid, auth_token)

def send_message(input_body, input_to):
    message = client.messages \
                    .create(
                        body=input_body,
                        from_=get_phone_number(),
                        to=input_to
                    )

    print(message.sid)


