#For this code to work you need to install flask using either "pip install flask" or "sudo apt-get install python-flask"
#then you will be able to import the following things into your code
#they are a bunch of functions that you will learn how to use, though not all today
from flask import Flask, render_template, session, request, redirect, url_for
import security

#__name__ is a python variable that returns the name of the function that is running it
#__name__ will return "__main__" if the code is being run in the function it was originally written in
#This line initializes flask to run in this program
app = Flask(__name__)


#This code sets the next function to be executed when someone tries to access [yoururl].com/
@app.route('/')
def index():
    #This function is called index() because usually the defualt page of a website is referred to as the index
    #for the purposes of this demo we're going to simply redirect to /page1
    return redirect('/home')


@app.route('/home')
def home():
    #This is Page1, we want to return the html of page1 as a website so it can be served to the client
    #The default location for html in flask is /templates so if you put an html file in the /templates directory
    #You can access it easily
    #This code returns the website stored in main.html
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
        code = request.form['code']
        if (verifyUser(username,code) == True):
            return render_template("user.html")
        else:
            return render_template("verify.html", err="Error, verification code invalid")
            
#This code checks that you are running this in the main function
#Someone else imports this code because they want to use a function you wrote, the following code won't execute
if __name__ == '__main__':
    #The secret key is an encryption key for the traffic to and from your website.
    #normally you would store it offline so people can't just see it
    #but this is a demo
    app.secret_key = 'DONT PUT THIS ON GITHUB IF YOU WANT SECURITY'

    #finally this line runs the code
    #The first parameter is the place you want to run it
    #  0.0.0.0 is localhost: your current machine
    #  127.0.0.0 is private localhost(I think) you can use this if you don't want people accessing your website
    #the port number is the port on your network card that you want to use to access the internet for this program
    #To view this website in action you go to "localhost:8000" in your browser
    app.run('0.0.0.0', port=8000)


#Ok That's all the code out of the way
#To execute the code just run python app.py
#This will run a networking server in the terminal
#To terminate the server press ctrl+c
#Keep in mind the server needs to be restarted for any changes you make to take effect
