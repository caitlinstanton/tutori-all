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

#returns true if the lists have at least one element in common
def listHasMatch(list1, list2):
    try:
        for x in list1:
            if x in list2:
                return True
            return False
    except:
        return False

#gets a list of tutors who are comfortable tutoring in classname, and have a free period matching at least one period listing in freesList
def getTutorList(classname, freesList):
    try:
        ans = []
        tutors = db.users.find({})
        for x in tutors:
            if x["numTuts"] > 0 and classname in x["goodClasses"] and listHasMatch(freesList,x["frees"]):
                ans.append(x)
        return ans
    except:
        return []

#returns a list of all the tutors that have the matching teacher from the classMatchList
#returns the empty list of none are found
def findTeacherMatches(classMatchList, teacherName):
    try:
        ans = []
        for tutor in classMatchList:
            if teacherName in tutor["goodClasses"]:
                ans.append(tutor)
        return ans
    except:
        return []

#chooses a random tutor that is willing to teach className, and has a free period listed in freesList
#Will pick a tutor that has the listed teacher, if one is available
#Returns the empty list if no tutors are available
def pickTutor(className, teacherName, freesList):
    try:
        tutorList = getTutorList(className)
        teacherMatches = findTeacherMatches(tutorList, "teacherName")
        if len(teacherMatches) > 0:
            tutorList = teacherMatches
        return random.choice(tutorList)
    except:
        return []
