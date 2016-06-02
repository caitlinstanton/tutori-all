from logs import log
from flask import Flask, render_template, session, request, redirect, url_for
from security import *
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/home')


@app.route('/home')
def home():
    return render_template("base.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        logged_in = security.authenticate(username, password)
        if logged_in:
            session['logged_in'] = True
            # session['userid'] = userid
            return redirect(url_for('home'))
        else:
            return render_template("login.html", err="Incorrect password or username")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    # session.pop('userid', None)
    return redirect("login")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    try:
        if request.method == "POST":
            log("sys","POST REQUEST RECEIVED AT /register")
            username = request.form['username']
            password = request.form['password']
            counselor = request.form['guidanceCounselor']
            homeroom = request.form['homeroomA'] + request.form['homeroomB']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            log("sys","all form data received")
            if (request.form['password2'] != password):
                log(username,"passwords didn't match, dickhead")
                return render_template("login.html", err="Error, passwords are not the same")

            else:
    			#print username + " " + password
    			#addedUser = utils.addUser(username, password) #boolean if user could be added
                log("sys", "account creation initialized")
                account = createAccount(username, password, counselor, homeroom, firstName, lastName)
                if (account == "Email in use"): #user already existed in the database.
                    log(username,"email in use")
                    return render_template("login.html", err="Email already in use")
                return redirect(url_for('verify'))
        else:
            return render_template("login.html")
    except:
        log("sys",sys.exc_info()[0])
@app.route('/verify', methods = ['GET', 'POST'])
def verify():
    if request.method == "POST":
        if 'username' in session:
            username = session['username']
            code = request.form['code']
            if (verifyUser(username,code) == True):
                return render_template("user.html")
            else:
                return render_template("verify.html", err="Error, verification code invalid")
        else:
            return render_template(url_for('login'))

if __name__ == '__main__':
    app.secret_key = 'DONT PUT THIS ON GITHUB IF YOU WANT SECURITY'
    app.run('0.0.0.0', port=8000)
