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
         return True
      else:
         log("sys","an unknown error accured during account creation")
         return False

#verifies an email address using random code generated during account creatio
def verifyUser(username, code):
   try:
      user = db.users.find({"username" : username})[0]
      if user["verificationCode"] == code:
         log(username,"account verified successully")
         user["isVerified"] = True
         db.users.update({"username": username}, user)
         return True
      else:
         log(username,"account verification failed; incorrect verification code")
         return False
   except:
      log(username,"unknown account verification error occurred")
      return False

#Adds a user to database
def addUser(username, password, counselor, homeroom, firstName, lastName, emailVerificationCode):
   print "addUser called"
   try:
      user = {"username": username, "hash": hashPass(password), "verificationCode": emailVerificationCode, "isVerified": False,
              "credits": {}, "isTutor": True, "classes": {},
              "guidanceCounselor": counselor, "homeRoom": homeroom,
              "frees":[], "goodClasses":[],
              "firstName": firstName, "lastName":lastName}

      print "user dict instantiated"
      try:
         db.users.insert(user)
      except:
         print "I KNEW IT"
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

#print createAccount("jijiglobe@gmail.com", "passpass", "blumm", "7RR", "Jion", "Fairchild")

# print authenticate("jijiglobe@gmail.com","passpass")
# print verifyUser("jijiglobe@gmail.com","s92nF5YLddhfcc0S2ing")
# print authenticate("jijiglobe@gmail.com","passpass")
