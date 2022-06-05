# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                    body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                    from_='+15017122661',
                    to='+15558675310'
                )

print(message.sid)
echo "export TWILIO_ACCOUNT_SID='ACa7499b15ba4968cb548d8205b6038a2f'" > twilio.env
echo "export TWILIO_AUTH_TOKEN='28acd2b273db970548bce4d3be0165e8'" >> twilio.env
source ./twilio.env
