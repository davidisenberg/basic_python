from flask import Flask
from flask import request
import sender

app = Flask(__name__)

@app.route('/')
def hello():
    return "David says hello"

@app.route('/send/')
def send():
    username = request.args.get('user')
    message = request.args.get('message')

    try:
        if username == "nothingbutnet":
            sender.send_message(message,"defined")
        else:
            return "unauthorized"
        return "sent message"
    except Exception as e:
        return "failed to send: " + str(e)



if __name__ == '__main__':
    app.run()