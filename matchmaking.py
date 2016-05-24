from security import *

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
        users["frees"] = freesList
        db.users.update({"username":username},user)
        log(username, "updated free period list")
        return True
    except:
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

def getTutorList(classname):
    try:
        ans = []
        tutors = db.users.find({})
        for x in tutors:
            if x["numTuts"] > 0 and classname in x["goodClasses"]:
                ans.append(x)
        return ans
    except:
        return []


def findTeacherMatches(classMatchList, teacherName):
    try:
        ans = []
        for tutor in classMatchList:
            if teacherName in tutor["goodClasses"]:
                ans.append(tutor)
        return ans
    except:
        return []

def pickTutor(className, teacherName, freesList):
    try:
        tutorList = getTutorList(className)
        teacherMatches = 
