from flask import Flask
from flask import request
import sender
import recipients

#https://help.pythonanywhere.com/pages/Flask/


app = Flask(__name__)



@app.route('/')
def hello():
    return "David says hello"

@app.route('/send/')
def send():
    username = request.args.get('user')
    message = request.args.get('message')

    recipient_list = recipients.get_recipients(username)
    if len(recipient_list) == 0:
        return "invalid username"

    for to in recipient_list:
        try:
            sender.send_message(message,to)
            
        except Exception as e:
            return "failed to send: " + str(e)
        
        return "sent message"

if __name__ == '__main__':
    app.run()
    