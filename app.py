from logs import log
from flask import Flask, render_template, session, request, redirect, url_for
from security import *

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
            return render_template("login.html#login", err="Incorrect password or username")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    # session.pop('userid', None)
    return redirect("login")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        log("sys","POST REQUEST RECEIVED AT /register")
        username = request.form['username']
        print username
        password = request.form['password']
        print password
        counselor = request.form['guidanceCounselor']
        print counselor
        homeroom = request.form['homeroomA'] + request.form['homeroomB']
        print homeroom
        firstName = request.form['firstName']
        print firstName
        lastName = request.form['lastName']
        print lastName
        log("sys","all form data received")
        if (request.form['password2'] != password):
            log("sys","passwords didn't match, dickhead")
            print "passwords didnt match"
            return render_template("login.html#signup", err="Error, passwords are not the same")

        else:
			#print username + " " + password
			#addedUser = utils.addUser(username, password) #boolean if user could be added
            log("sys", "account creation initialized")
            account = createAccount(username, password, counselor, homeroom, firstName, lastName)
            print "account creation successful"
            if (account == "Email in use"): #user already existed in the database.
                print "email in use"
                log(username,"account creation successful")
                return render_template("login.html#signup", err="Account creation not successful")
            print "supposedly redirects to login"
            return redirect(url_for('login'))
    else:
        return render_template("login.html#signup")

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
