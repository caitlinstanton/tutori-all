from security import *
import time
from globalVars import *
from matchmaking import *

#gets the current date in the mm-dd-yy format
def getDate():
    return time.strftime("%m-%d-%y")

#gets a unique name to represent a session with the given parameters
def getSessionName(tutorName, tuteeName, date):
    return "%s - %s - %s" % (tutorName, tuteeName, date)

#returns a boolean representing whether a session with the given specs exists
def sessionExists(tutorName, tuteeName, Date):
    try:
        name = getSessionName(tutorName, tuteeName, Date)
        #print name
        x = db.sessions.find({"sessionName": name})
        for var in x:
            return True
        return False
    except:
        print "ERROR BOIS"
        return False

#session submission function that should be used by tutees
#  If the tutor has not yet submitted the session, it creates the session with the given information and "isConfirmed": False
#  If the tutor has submitted the session, and the information matches, it will confirm the session by setting "isConfirmed": True
#  If the tutor and tutee submit different information, it'll email them about the issue and ask them to fix it.
def submitSessionAstutee(tutorName, tuteeName, length, date, location):
    found = sessionExists(tutorName, tuteeName, date)
    name = getSessionName(tutorName, tuteeName, date)
    if found:
        sess = db.sessions.find({"sessionName": name})[0]
        sess["tuteeLength"] = length
        sess["tuteeLocation"] = location
        lengthMatch = not sess["tutorLength"] == sess["tuteeLength"]
        locationMatch = not sess["tutorLocation"] == sess["tuteeLocation"]
        print "locationMatch"+str(locationMatch)
        print "lengthMatch"+str(lengthMatch)

        tutor = db.users.find({"username":tutorName})[0]
        tutee = db.users.find({"username":tuteeName})[0]

        tutorFirstName = tutor["firstName"]
        tuteeFirstName = tutee["firstName"]

        if lengthMatch and locationMatch:
            #neither match
            error = "the session lengths and locations you submitted did not match"
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tuteeFirstName, error))
            email(tuteeName,"issue processing session",missmatchSessionEmail % (tuteeFirstName, tutorFirstName, error))
            return "length and location mismatch"

        elif lengthMatch:
            #length doesn't match
            error = "the session lengths you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tuteeFirstName, error))
            email(tuteeName,"issue processing session",missmatchSessionEmail % (tuteeFirstName, tutorFirstName, error))
            return "length mismatch"

        elif locationMatch:
            #locationMatch
            error = "the locations you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tuteeFirstName, error))
            email(tuteeName,"issue processing session",missmatchSessionEmail % (tuteeFirstName, tutorFirstName, error))
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
                "tuteeName": tuteeName,
                "date": date,
                "tuteeLength": length,
                "tuteeLocation": location,
                "isConfirmed": False}
        db.sessions.insert(sess)
        return "session created"

#session submission function that should be used by tutors
#  If the tutee has not yet submitted the session, it creates the session with the given information and "isConfirmed": False
#  If the tutee has submitted the session, and the information matches, it will confirm the session by setting "isConfirmed": True
#  If the tutee and tutee submit different information, it'll email them about the issue and ask them to fix it.
def submitSessionAsTutor(tutorName, tuteeName, length, date, location):
    found = sessionExists(tutorName, tuteeName, date)
    name = getSessionName(tutorName, tuteeName, date)
    if found:
        sess = db.sessions.find({"sessionName": name})[0]
        sess["tutorLength"] = length
        sess["tutorLocation"] = location
        lengthMatch = not sess["tutorLength"] == sess["tuteeLength"]
        locationMatch = not sess["tutorLocation"] == sess["tuteeLocation"]
        print "locationMatch"+str(locationMatch)
        print "lengthMatch"+str(lengthMatch)
        tutor = db.users.find({"username":tutorName})[0]
        tutee = db.users.find({"username":tuteeName})[0]

        tutorFirstName = tutor["firstName"]
        tuteeFirstName = tutee["firstName"]

        if lengthMatch and locationMatch:
            #neither match
            error = "the session lengths and locations you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tuteeFirstName, error))
            email(tuteeName,"issue processing session",missmatchSessionEmail % (tuteeFirstName, tutorFirstName, error))
            return "length and location mismatch"

        elif lengthMatch:
            #length doesn't match
            error = "the session lengths you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tuteeFirstName, error))
            email(tuteeName,"issue processing session",missmatchSessionEmail % (tuteeFirstName, tutorFirstName, error))
            return "length mismatch"

        elif locationMatch:
            #locationMatch
            error = "the locations you submitted did not match"
            #print error
            email(tutorName,"issue processing session",missmatchSessionEmail % (tutorFirstName, tuteeFirstName, error))
            email(tuteeName,"issue processing session",missmatchSessionEmail % (tuteeFirstName, tutorFirstName, error))
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
                "tuteeName": tuteeName,
                "date": date,
                "tutorLength": length,
                "tutorLocation": location,
                "isConfirmed": False}
        db.sessions.insert(sess)
        return "session created"

db.sessions.remove({})
"""print submitSessionAsTutor("Jion","Caitlin",1,"12-12-12","fuck")
print submitSessionAstutee("Jion","Caitlin",1,"12-12-12","fuck")
print "you should see session created, then match\n"

print submitSessionAstutee("Jion1","Caitlin",1,"12-12-12","fuck")
print submitSessionAsTutor("Jion1","Caitlin",1,"12-12-12","fuck")
print "you should see session created, then match\n"


print submitSessionAsTutor("Jion2","Caitlin",1,"12-12-12","fuc")
print submitSessionAstutee("Jion2","Caitlin",1,"12-12-12","fuck")
print "you should see session created, then location mismatch\n"

print submitSessionAsTutor("Jion3","Caitlin",1,"12-12-12","fuck")
print submitSessionAstutee("Jion3","Caitlin",2,"12-12-12","fuck")
print "you should see session created, then length mismatch\n"

print submitSessionAsTutor("Jion4","Caitlin",1,"12-12-12","fuc")
print submitSessionAstutee("Jion4","Caitlin",2,"12-12-12","fuck")
print "you should see session created, then double mismatch\n"
"""
