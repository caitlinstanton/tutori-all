from logs import log
from flask import Flask, render_template, session, request, redirect, url_for
from security import *
from matchmaking import *
import sys
from globalVars import *
import json, codecs

app = Flask(__name__)
app.debug = True

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
        print "start authenticate"
        try:
            logged_in = authenticate(username, password)
        except:
            print sys.exc_info()[0]
        print "done authenticate"
        if logged_in:
            print "logged_in = true"
            session['logged_in'] = True
            print "add logged_in to session"
            session['username'] = username
            print "add username to session"
            # session['userid'] = userid
            try:
                return redirect(url_for('user'))
                #print "redirect to user settings page"
                #return render_template("user.html")
            except:
                print sys.exc_info()[0]
        else:
            return render_template("login.html", err="Incorrect password or username")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
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
                log(username,"passwords didn't match")
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
    if request.method == "GET" and request.args.get('code') != None:
        print "GET"
        # username = session['username']
        code = request.args.get('code')
        print "code: %s" % code
        username = verifyUser(code)
        print "username: %s" % username
        if (username != "" and 'username' not in session):
            session['username'] = username
            #return render_template("user.html")
            return redirect(url_for('user'))
        else:
            return render_template("verify.html", err="Error, verification code invalid")
    else:
        return render_template("verify.html")

@app.route('/user')
def user():
    #session = requests.Session()
    # username = session["username"]
    # user = db.user.find({"username":username})[0]

    if 'username' in session:
        # print "username is in session"
        username = session['username']
        user = getUser(username)
        print user
        if request.method == "GET" and request.args.get("class") != None:

            classname = request.args.get("class")

            addGoodClass(username,classname,request.args.get(classname+"Teacher"))

        if request.method == "GET" and request.args.get("free")!=None:
            #choose frees here
            pass

        firstName = user['firstName']
        print "First Name: %s" % firstName

        lastName = user['lastName']
        homeRoom = user['homeRoom']
        goodClasses = user['goodClasses']
        credits = user['credits']
        numTuts = user['numTuts']
        classes = user['classes']
        guidanceCounselor = user['guidanceCounselor']
        phonenumber = "1234567890"
        isTutor = user['isTutor']

        print "isTutor: "
        print isTutor
        #status = "Tutee"
        #print "status: %s" % status
        ranking = 5
        if isTutor:
            # lookingFor = "Tutee"
            return render_template("tutor.html", ranking = ranking, username = username, firstName = firstName, lastName = lastName, phonenumber = phonenumber)
        else:
            # lookingFor = "Tutor"
            return render_template("tutee.html", username = username, firstName = firstName, lastName = lastName, phonenumber = phonenumber)
        #print "looking for: %s" % lookingFor
        # try:
        #     return render_template("user.html")
        # except:
        #     print sys.exc_info()[0]
        # try:
        #     return render_template("user.html", username = username, firstName = firstName, lastName = lastName, phonenumber = phonenumber, lookingFor = lookingFor)
        # except:
        #     print sys.exc_info()[0]
    else:
        print "username is not in session"
        return redirect(url_for('login'))

@app.route('/match')
def match():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        isTutor = user['isTutor']

        if isTutor:
            lookingFor = "Tutee"
        else:
            lookingFor = "Tutor"
            
        #print "class list: "

        #print classList
        #print classList['Pre-Calculus'][0]

        # for subject in classList:
        #     for teacher in subject:
        #
            # try:
            #     print classList[x][0]
            # except:
            #     print sys.exc_info()[0]
            #     print "there was nothing"
        try:
            return render_template("match.html", lookingFor = lookingFor)
            #return render_template("tutor.html", classList = classList, lookingFor = "tutor")#, lookingFor = "tutor")

        except:
            print "\n\n\n\n"
            print sys.exc_info()[0]
    else:
        return redirect(url_for('login'))

@app.route('/sessions')
def sessions():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        isTutor = user['isTutor']

        if isTutor:
            lookingFor = "Tutee"
            #sessions = db.users.find({"tutorName": username})[0]
        else:
            lookingFor = "Tutor"
            #sessions = db.users.find({"tuteeName": username})[0]

        print "sessions: "
        print sessions

        try:
            return render_template("sessions.html", lookingFor = lookingFor)
        except:
            print sys.exc_info()[0]
    else:
        return redirect(url_for('login'))

@app.route('/submit')
def submit():
    return render_template("submit.html")

@app.route('/pairings')
def pairings():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        isTutor = user['isTutor']
        if isTutor:
            lookingFor = "Tutee"
            matches = getValue(username, "tutees")
        else:
            lookingFor = "Tutor"
            matches = getValue(username, "tutors")
        try:
            return render_template("pairings.html", lookingFor = lookingFor, matches = matches)

        except:
            print sys.exc_info()[0]
    else:
        return redirect(url_for('login'))


def dictToJSON(dictionary):
    with codecs.open('%s.json' % str(dictionary), 'w', 'utf8') as f:
        f.write(json.dumps(dictionary, sort_keys = True, ensure_ascii=False))

if __name__ == '__main__':
    app.secret_key = 'DONT PUT THIS ON GITHUB IF YOU WANT SECURITY'
    app.run('0.0.0.0', port=8000)
