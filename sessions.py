from security import *
import time
from globalVars import *
from matchmaking import *

def getDate():
    return time.strftime("%m-%d-%y")


def getSessionName(tutorName, tutteeName, date):
    return "%s - %s - %s" % (tutorName, tutteeName, date)

def sessionExists(tutorName, tutteeName, Date):
    try:
        name = getSessionName(tutorName, tutteeName, Date)
        #print name
        x = db.sessions.find({"sessionName": name})
        for var in x:
            return True
        return False
    except:
        print "ERROR BOIS"
        return False

def submitSessionAsTuttee(tutorName, tutteeName, length, date, location):
    found = sessionExists(tutorName, tutteeName, date)
    name = getSessionName(tutorName, tutteeName, date)
    if found:
        sess = db.sessions.find({"sessionName": name})[0]
        sess["tutteeLength"] = length
        sess["tutteeLocation"] = location
        lengthMatch = not sess["tutorLength"] == sess["tutteeLength"]
        locationMatch = not sess["tutorLocation"] == sess["tutteeLocation"]
        print "locationMatch"+str(locationMatch)
        print "lengthMatch"+str(lengthMatch)

        tutor = db.users.find({"username":tutorName})[0]
        tuttee = db.users.find({"username":tutteeName})[0]
        
        tutorFirstName = tutor["firstName"]
        tutteeFirstName = tuttee["firstName"]
        
        if lengthMatch and locationMatch:
            #neither match
            error = "the session lengths and locations you submitted did not match"
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tutteeFirstName, error))
            email(tutteeName,"issue processing session",missmatchSessionEmail % (tutteeFirstName, tutorFirstName, error))           
            return "length and location mismatch"

        elif lengthMatch:
            #length doesn't match
            error = "the session lengths you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tutteeFirstName, error))
            email(tutteeName,"issue processing session",missmatchSessionEmail % (tutteeFirstName, tutorFirstName, error))
            return "length mismatch"
            
        elif locationMatch:
            #locationMatch
            error = "the locations you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tutteeFirstName, error))
            email(tutteeName,"issue processing session",missmatchSessionEmail % (tutteeFirstName, tutorFirstName, error))
            return "location mismatch"
            
        else:
            #everything matches
            sess["isConfirmed"] = True
            db.sessions.update({"sessionName":name},sess)
            #tutor["credits"]
            return "match"

    else:
        sess = {"sessionName": name,
                "tutorName": tutorName,
                "tutteeName": tutteeName,
                "date": date,
                "tutteeLength": length,
                "tutteeLocation": location,
                "isConfirmed": False}
        db.sessions.insert(sess)
        return "session created"

def submitSessionAsTutor(tutorName, tutteeName, length, date, location):
    found = sessionExists(tutorName, tutteeName, date)
    name = getSessionName(tutorName, tutteeName, date)
    if found:
        sess = db.sessions.find({"sessionName": name})[0]
        sess["tutorLength"] = length
        sess["tutorLocation"] = location
        lengthMatch = not sess["tutorLength"] == sess["tutteeLength"]
        locationMatch = not sess["tutorLocation"] == sess["tutteeLocation"]
        print "locationMatch"+str(locationMatch)
        print "lengthMatch"+str(lengthMatch)
        tutor = db.users.find({"username":tutorName})[0]
        tuttee = db.users.find({"username":tutteeName})[0]
        
        tutorFirstName = tutor["firstName"]
        tutteeFirstName = tuttee["firstName"]
        
        if lengthMatch and locationMatch:
            #neither match
            error = "the session lengths and locations you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tutteeFirstName, error))
            email(tutteeName,"issue processing session",missmatchSessionEmail % (tutteeFirstName, tutorFirstName, error))
            return "length and location mismatch"

        elif lengthMatch:
            #length doesn't match
            error = "the session lengths you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tutteeFirstName, error))
            email(tutteeName,"issue processing session",missmatchSessionEmail % (tutteeFirstName, tutorFirstName, error))
            return "length mismatch"
            
        elif locationMatch:
            #locationMatch
            error = "the locations you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tutteeFirstName, error))
            email(tutteeName,"issue processing session",missmatchSessionEmail % (tutteeFirstName, tutorFirstName, error))
            return "location mismatch"

        else:
            #everything matches
            #print "everything matched"
            sess["isConfirmed"] = True
            db.sessions.update({"sessionName":name},sess)
            tutor["credits"]
            return "match"
    else:
        #no session currently found
        sess = {"sessionName": name,
                "tutorName": tutorName,
                "tutteeName": tutteeName,
                "date": date,
                "tutorLength": length,
                "tutorLocation": location,
                "isConfirmed": False}
        db.sessions.insert(sess)
        return "session created"
        
db.sessions.remove({})
"""print submitSessionAsTutor("Jion","Caitlin",1,"12-12-12","fuck")
print submitSessionAsTuttee("Jion","Caitlin",1,"12-12-12","fuck")
print "you should see session created, then match\n"

print submitSessionAsTuttee("Jion1","Caitlin",1,"12-12-12","fuck")
print submitSessionAsTutor("Jion1","Caitlin",1,"12-12-12","fuck")
print "you should see session created, then match\n"

"""
print submitSessionAsTutor("Jion2","Caitlin",1,"12-12-12","fuc")
print submitSessionAsTuttee("Jion2","Caitlin",1,"12-12-12","fuck")
print "you should see session created, then location mismatch\n"

print submitSessionAsTutor("Jion3","Caitlin",1,"12-12-12","fuck")
print submitSessionAsTuttee("Jion3","Caitlin",2,"12-12-12","fuck")
print "you should see session created, then length mismatch\n"

print submitSessionAsTutor("Jion4","Caitlin",1,"12-12-12","fuc")
print submitSessionAsTuttee("Jion4","Caitlin",2,"12-12-12","fuck")
print "you should see session created, then double mismatch\n"

