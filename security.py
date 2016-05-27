import sys
from logs import *
from passlib.hash import pbkdf2_sha256
import pymongo
from pymongo import MongoClient
import random, string
from globalVars  import *

connection = MongoClient()
db = connection.database

#generates a random lowercase String
def generateRandomString(length):
   return ''.join(random.choice(string.lowercase+string.ascii_uppercase+string.digits) for i in range(length))

#Runs full account creation script and returns message indicating operation status
def createAccount(username, password, counselor, homeroom, firstName, lastName):
   try:
      print "create got run"
      if checkUsername(username):
         log(username, "attempted account creation")
         return "Email in use"
      else:
         code = generateRandomString(20)
         print "code generated"
         if addUser(username, password, counselor, homeroom, firstName, lastName, code):
            print "user added"
            log(username, "account created")
            email(username,"Stuy Arista Account Creation",accountCreationEmail % (firstName, code))
            return "success"
         else:
            log("sys","an unknown error accured during account creation")
            return "error"
   except:
      log(username, "this should never ever happen")
      return "error"
#verifies an email address using random code generated during account creation
#returns username upon successful completion, returns empty string otherwise
def verifyUser(code):
   try:
      user = db.users.find({"verificationCode" : code})[0]
      username = user["username"]
      if user["verificationCode"] == code:
         log(username,"account verified successully")
         user["isVerified"] = True
         db.users.update({"username": username}, user)
         return username
      else:
         log(username,"account verification failed; incorrect verification code")
         return ""
   except:
      log(username,"unknown account verification error occurred")
      return ""

#Adds a user to database
def addUser(username, password, counselor, homeroom, firstName, lastName, emailVerificationCode):
   try:
      user = {"username": username, "hash": hashPass(password), "verificationCode": emailVerificationCode, "isVerified": False,
              "credits": {}, "isTutor": True, "classes": {},
              "guidanceCounselor": counselor, "homeRoom": homeroom,
              "frees":[], "goodClasses":[],"numTuts": 0,
              "firstName": firstName, "lastName":lastName}

      try:
         db.users.insert(user)
      except:
         return False
      return True
   except:
      print sys.exc_info()[0]
      return False

#Returns boolean that indicates whether a user has inputted correct login information
def authenticate(username, password):
   try:
      user = db.users.find({"username": username})
      check = verify(password,user[0]["hash"]) and user[0]["isVerified"]
      if check:
         log(username,"logged in")
         return True
      else:
         log(username,"failed login was attempted")
         return False
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
   print "hashPass called"
   encrypted = pbkdf2_sha256.encrypt(password)
   print "hash generated"
   return encrypted

# Returns true if password hashes into hashpass, false otherwise
def verify(password, hashpass):
   return pbkdf2_sha256.verify(password,hashpass)

#Requests a password reset, returns True upon successful completion
def requestPasswordReset(username):
   try:
      user = db.users.find({"username": username})[0]
      log(username,"Requested password reset")
      code = generateRandomString(20)
      user["verificationCode"] = code
      pass
   except:
      pass

for x in range(10):
   createUser("User"+str(x), "pass", "Wu", "7RR","Jion"+str(x), "Fair")
