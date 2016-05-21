from logs import log
from passlib.hash import pbkdf2_sha256
import pymongo
from pymongo import MongoClient

#Runs full account creation script and returns message indicating operation status
def createAccount(username, password, counselor, homeroom, firstName, lastName):
    if checkUsername(username,password):
        log(username, "attempted account creation")
        return "Email in use"
    else:
        if addUser(username, password, counselor, homeroom, firstName, lastName):
            log(username, "account created")
            return "Account creation successful"
        else:
            log("sys","an unknown error accured during account creation")
            return "Account creation failed"

#Adds a user to database
def addUser(username, password, counselor, homeroom, firstName, LastName):
    try:
        user = {"username": username, "hash": hashPass(password) "credits": {}, "isTutor": True,"classes": {},
                "guidanceCounselor": counselor,"homeRoom":homeroom,
                "frees":[],"goodClasses":[],
                "firstName": firstName, "lastName":lastName}
        db.users.insert(user)
        return True
    except:
        return False

#Returns boolean that indicates whether a user has inputted correct login information
def authenticate(username, password):
    try:
        user = db.users.find({"name": username})
        check = verify(password,user[0]["hash"])
        if check:
            log(username,"logged in")
        else:
            log(username,"failed login was attempted")
    except:
        log(username, "an unknown user authentication error occurred")
        return False

#Returns boolean indicating whether a certain username is taken
def checkUsername(username):
    try:
        user = db.users.find({"name": username})
        if len(users >=1):
            return True
        else:
            return False
    except:
        return False

#Removes user from the database
def deleteUser(username):
    pass

# Hashes and returns password that is hashed and salted by 29000 rounds of pbkdf2 encryption                                          
def hashPass(password):
    return pbkdf2_sha256.encrypt(password)

# Returns true if password hashes into hashpass, false otherwise                                                                      
def verify(password, hashpass):
    return pbkdf2_sha256.verify(password,hashpass)
