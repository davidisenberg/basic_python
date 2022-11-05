import os
from twilio.rest import Client

# Download the helper library from https://www.twilio.com/docs/python/install
# ? Shorthand identifier for your profile: My first Twilio account
# Created API Key SK771f8a8e2cc65eee00220c112495c55e and stored the secret in Config. See: https://www.twilio.com/console/runtime/api-keys/SK771f8a8e2cc65eee00220c112495c55e
# twilio-cli configuration saved to "C:\Users\david\.twilio-cli\config.json"
# Saved My first Twilio account.
#  You don't have any active profile set, run "twilio profiles:use" to set a profile as active

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# https://www.twilio.com/blog/register-phone-number-send-sms-twilio-cli
# twilio profiles:use "My first Twilio account"
# twilio api:core:incoming-phone-numbers:create --phone-number="+14846015086"

account_sid = 'ACb42f9115cf27b3c34ddfc388e381aeee' #os.environ['ACb42f9115cf27b3c34ddfc388e381aeee']
auth_token = 'da3421679cdd3837e09526998e6f26cf' #os.environ['da3421679cdd3837e09526998e6f26cf']
client = Client(account_sid, auth_token)

def send_message(input_body, input_to):
    message = client.messages \
                    .create(
                        body=input_body,
                        from_='+14846015086',
                        to='+17189862989'
                    )

    print(message.sid)


