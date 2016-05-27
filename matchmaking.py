import sys
from security import *

def changeValue(username,variable, value):
    user = db.users.find({"username": username})[0]
    user[variable] = value
    db.users.update({"username":username}, user)

#changes selected user into a tutor
def makeTutor(username):
    changeValue(username,"isTutor",True)
    

#adds a class to a users "classes that I wish to tutor in" list
#classes are tuples that contain the name of the class, and the teacher they had
def addGoodClass(username, classname, teacher):
    try:
        user = db.users.find({"username": username})[0]
        classTuple = (classname, teacher)
        user["goodClasses"].append(classTuple)
        db.users.update({"username": username},user)
        log(username,"added "+classname+" taught by "+ teacher)
        return True
    except:
        log(username,"error encountered when adding a class to goodClassList")
        return False

#sets a user's free periods to a given list
#To set jion@jion.net's free periods to 1st, 6th and 10th, use chooseFrees("jion@jion.net",[1,6,10])
def chooseFrees(username, freesList):
    try:
        user = db.users.find({"username": username})[0]
        user ["frees"] = freesList
        db.users.update({"username":username},user)
        log(username, "updated free period list")
        return True
    except:
        print sys.exc_info()[0]
        log(username, "error when updating frees")
        return False


#returns free periods list of the user
def getFrees(username):
    try:
        return db.users.find({"username":username})[0]["frees"]
    except:
        log(username,"unable to retrieve free period list")

#returns list of good classes as tuples in the following format:
#  (classname, teacher)
def getGoodClassList(username):
    try:
        return db.users.find({"username":username})[0]["goodClasses"]
    except:
        log(username, "unable to retrieve good class list")

#returns true if the lists have at least one element in common
def listHasMatch(list1, list2):
    try:
        for x in list1:
            if x in list2:
                return True
            return False
    except:
        return False

def hasClass(userdict,classname):
    for x in userdict["goodClasses"]:
        if classname in x:
            return True
    return False


#gets a list of tutors who are comfortable tutoring in classname, and have a free period matching at least one period listing in freesList
def getTutorList(classname, freesList):
    try:
        print "getTutorlist initialized"
        ans = []
        tutors = db.users.find({})
        for x in tutors:
            #print x
            #print x["numTuts"] > 0
            #print hasClass(x,classname)#classname#x["goodClasses"]#classname in x["goodClasses"]
            #print listHasMatch(freesList,x["frees"])

            if x["numTuts"] > 0 and hasClass(x,classname) and listHasMatch(freesList,x["frees"]):
               ans.append(x)
        #print ans
        return ans
    except:
        print "getTutorList crashed"
        print sys.exc_info()[0]
        return []

#returns a list of all the tutors that have the matching teacher from the classMatchList
#returns the empty list of none are found
def findTeacherMatches(classMatchList, teacherName):
    try:
        ans = []
        for tutor in classMatchList:
            #print teacherName
            #print hasClass(tutor,teacherName)
            if hasClass(tutor,teacherName):
                ans.append(tutor)
                print "appended"
        return ans
    except:
        print sys.exc_info()[0]
        return []


#chooses a random tutor that is willing to teach className, and has a free period listed in freesList
#Will pick a tutor that has the listed teacher, if one is available
#Returns the empty list if no tutors are available
def pickTutor(className, teacherName, freesList):
    try:
        print "pick called"
        tutorList = getTutorList(className,freesList)
        print "tutorlist generated"
        #print "TutorList: "+str(tutorList)
        teacherMatches = findTeacherMatches(tutorList, teacherName)
        #print "teacherMatches: "+ str(teacherMatches)
        for x in teacherMatches:
            tutorList = teacherMatches
            break
        return random.choice(tutorList)
    except:
        pass

print pickTutor("physics","Ali",[2,4])
