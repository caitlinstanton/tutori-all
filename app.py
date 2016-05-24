from flask import Flask, render_template, session, request, redirect, url_for
import security

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
        username = request.form['username']
        password = request.form['password']
        counselor = request.form['guidanceCounselor']
        homeroom = request.form['homeroomA'] + request.form['homeroomB']
        firstName = request.form['firstName']
        lastName = request.form['lastName']

        if (request.form['password2'] != password):
            return render_template("login.html#signup", err="Error, passwords are not the same")
        else:
			#print username + " " + password
			#addedUser = utils.addUser(username, password) #boolean if user could be added
            account = createAccount(username, password, counselor, homeroom, firstName, lastName)
            if (not account): #user already existed in the database.
				return render_template("login.html#signup", err="Account creation not successful")
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
