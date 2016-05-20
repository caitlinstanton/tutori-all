from passlib.hash import pbkdf2_sha256
import pymongo
from pymongo import MongoClient

#Adds a user to database
def addUser(username, password, counselor, homeroom):
    try:
        user = {"name": username, "hash": hashPass(password) "credits": {}, "isTutor": True,"classes": {},
                "guidanceCounselor": counselor,"homeRoom":homeroom,"frees":[],"goodClasses":[]}
        db.users.insert(users)
        return True
    except:
        return False

#Returns boolean that indicates whether a user has inputted correct login information
def authenticate(username, password):
    try:
        user = db.users.find({"name": username})
        return verify(password,user[0]["hash"])
    except:
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
