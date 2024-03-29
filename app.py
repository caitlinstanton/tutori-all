from logs import log
from flask import Flask, render_template, session, request, redirect, url_for
from security import *
from matchmaking import *
import sys
from globalVars import *
import json, codecs
from crediting import *

app = Flask(__name__)
#app.debug = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = "SUPER DUPER REALLY SECRET"

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template("base.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session:
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
    else:
        return redirect(url_for('user'))

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    # session.pop('userid', None)
    return redirect(url_for("login"))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if 'username' not in session:
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
    else:
        return redirect(url_for('user'))

@app.route('/verify', methods = ['GET', 'POST'])
def verify():
    if 'username' not in session:
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
    else:
        return redirect(url_for('user'))

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
        isAdmin = user['isAdmin']

        print "isTutor: "
        print isTutor
        #status = "Tutee"
        #print "status: %s" % status
        ranking = 5

        if isTutor and not isAdmin:
            # lookingFor = "Tutee"
            return render_template("tutor.html", ranking = ranking, username = username, firstName = firstName, lastName = lastName, phonenumber = phonenumber)
        elif not isTutor and not isAdmin:
            # lookingFor = "Tutor"
            return render_template("tutee.html", username = username, firstName = firstName, lastName = lastName, phonenumber = phonenumber)
        else:
            return redirect(url_for('adminSessions'))
    else:
        print "username is not in session"
        return redirect(url_for('login'))

@app.route('/match')
def match():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        print user
        isTutor = user['isTutor']

        if not isTutor:
            try:
                className = request.form['class']
                teacherName = request.form['teacher']
                freesList = request.form['freesList']
                tutor = pickTutor(className, teacherName, freesList)
                addTutor(username, (tutor, className, teacherName))
                addTutee(tutor, (username, className, teacherName))
            except:
                print sys.exc_info()[0]

            try:
                return render_template("match.html")
            except:
                print sys.exc_info()[0]
        else:
            try:
                return redirect(url_for('user'))
            except:
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
            try:
                sessions = db.sessions.find({"tutorName": username})[0]
            except:
                sessions = "NONE"
                print sys.exc_info()[0]
        else:
            lookingFor = "Tutor"
            try:
                sessions = db.sessions.find({"tuteeName": username})[0]
            except:
                sessions = "NONE"
                print sys.exc_info()[0]

        print "sessions: "
        print sessions

        try:
            return render_template("sessions.html", lookingFor = lookingFor)
        except:
            print sys.exc_info()[0]
    else:
        return redirect(url_for('login'))

@app.route('/adminSessions')
def adminSessions():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        isAdmin = user['isAdmin']

        sessions = db.sessions.find({})

        if isAdmin:
            return render_template("adminSessions.html", sessions = sessions)
        else:
            return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        print user
        isTutor = user['isTutor']
        isAdmin = user['isAdmin']

        if not isAdmin and isTutor:
            lookingFor = "Tutee"
        elif not isAdmin and not isTutor:
            lookingFor = "Tutor"
        else:
            return redirect(url_for('user'))

        if request.method == "POST":
            email = request.form["email"]
            date = request.form["date"]
            startTime = request.form["startTime"]
            endTime = request.form["endTime"]
            location = request.form["place"]
            length = (endTime - startTime)/60

            if isTutor:
                submitSessionAsTutor(username, email, length, date, location)
            else:
                submitSessionAsTutee(username, email, length, date, location)

        else:
            return render_template("submit.html", lookingFor = lookingFor)
    else:
        return redirect(url_for('login'))


@app.route('/pairings')
def pairings():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        isTutor = user['isTutor']
        isAdmin = user['isAdmin']

        if isTutor:
            lookingFor = "Tutee"
            match = getValue(username, "tutees")
        # elif(isAdmin):
        #     lookingFor = "Tutor and Tutee"
        #     match = getValue()
        else:
            lookingFor = "Tutor"
            match = getValue(username, "tutors")

        try:
            return render_template("pairings.html", lookingFor = lookingFor, match = match)

        except:
            print sys.exc_info()[0]
    else:
        return redirect(url_for('login'))

@app.route('/adminPairings')
def adminPairings():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        isAdmin = user['isAdmin']

        users = db.users.find({})
        print users[0]['isAdmin']

        if isAdmin:
            return render_template("adminPairings.html", users = users)
        else:
            return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))

@app.route('/adminCredits')
def adminCredits():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        isAdmin = user['isAdmin']

        users = db.users.find({})


        if isAdmin:
            return render_template("adminCredits.html", users = users)
        else:
            return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))

@app.route('/adminTrimester', methods=['GET', 'POST'])
def adminTrimester():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        isAdmin = user['isAdmin']
        if request.method == "POST" and isAdmin:


            trimesterList = getTrimesterList()
            trimesterListChanges = []

            trimesterListChanges.append(request.form['tri1start'])
            trimesterListChanges.append(request.form['tri1end'])
            trimesterListChanges.append(request.form['tri2start'])
            trimesterListChanges.append(request.form['tri2end'])
            trimesterListChanges.append(request.form['tri3start'])
            trimesterListChanges.append(request.form['tri3end'])

            count = 0
            for trimester in trimesterListChanges:
                if trimester != "":
                    changeTrimester(trimesterList[count], trimester)
                    count += 1

        elif request.method == "GET" and isAdmin:
            return render_template("adminTrimester.html")
        else:
            return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))

@app.route('/adminChangeUser', methods=['GET', 'POST'])
def adminChangeUser():
    if 'username' in session:
        username = session['username']
        user = getUser(username)
        isAdmin = user['isAdmin']

        actionDone = ""

        if request.method == "GET" and isAdmin and request.args.get('username') != None and request.args.get('changeUser') != None:
            userChanging = request.args.get('username')
            userAction = request.args.get('changeUser')

            if userAction == "makeTutor":
                changeValue(userChanging, "isTutor", True)
                actionDone = "Made user a tutor"
            if userAction == "removeTutor":
                changeValue(userChanging, "isTutor", False)
                actionDone = "Made user not a tutor"

            return render_template("adminChangeUser.html", actionDone = actionDone)
        elif request.method == "GET" and isAdmin:
            return render_template("adminChangeUser.html")
        else:
            return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))


def dictToJSON(dictionary):
    with codecs.open('%s.json' % str(dictionary), 'w', 'utf8') as f:
        f.write(json.dumps(dictionary, sort_keys = True, ensure_ascii=False))

if __name__ == '__main__':
    #app.secret_key = 'DONT PUT THIS ON GITHUB IF YOU WANT SECURITY'
    app.run('0.0.0.0', port=8000)
