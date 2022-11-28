from flask import Flask, request, render_template,  session, g, Response, redirect, url_for, abort
import sender
import recipients
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user

from datetime import timedelta

#https://help.pythonanywhere.com/pages/Flask/


app = Flask(__name__)

# flask-login
#https://mulgrew.me/posts/session-timeout-flask.html
#https://flask-login.readthedocs.io/en/latest/#how-it-works
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "register"

# silly user model
class User(UserMixin):

    def __init__(self, phone):
        self.phone = phone
        self.id = phone
        
        
    def __repr__(self):
        return "%s" % (self.id)


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
            #print("would have sent")
            sender.send_message(message,to)
            
        except Exception as e:
            return "failed to send: " + str(e)
        
    return render_template('./response.html')


@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        phone = request.form['phone']
        user = User(phone)
        login_user(user)
        return redirect(request.args.get("next"))
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=phone>
            <p><input type=submit value=Login>
        </form>
        ''')


@app.route('/beta/')
@login_required
def beta():

    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
    session.modified = True
    g.user = current_user
    print("user" + str(g.user.phone))

    recipient_list = recipients.get_recipients(current_user)
    if len(recipient_list) == 0:
        return "invalid username"

    for to in recipient_list:
        try:
            print("would have sent")
            #sender.send_message("testing",to)
            
        except Exception as e:
            return "failed to send: " + str(e)
        
    return render_template('./response.html')

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
    session.modified = True
    g.user = current_user

# callback to reload the user object        
@login_manager.user_loader
def load_user(phone):
    return User(phone)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

if __name__ == '__main__':
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    # https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    #app.debug = True
    app.run()
    