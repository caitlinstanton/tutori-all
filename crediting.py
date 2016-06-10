from security import *
import time
import datetime

twoWeeks = 15 * 60 * 60 * 24

#initializes first two trimesters
def initializeTrimesters(trimester1,trimester2):
    db.globals.insert({"name":"trimesters", 
                       "value":[getUnixTime(trimester1),getUnixTime(trimester2)] })

#gets a list in unix time of start dates for trimesters
def getTrimesterList():
    return db.globals.find({"name":"trimesters"})[0]["value"]

#adds a trimester to the trimester list
def addTrimester(date):
    globalData = db.globals.find({"name":"trimesters"})[0]
    trimesterList = getTrimesterList()
    trimesterList.append(getUnixTime(date))
    globalData["value"] = trimesterList
    db.globals.update({"name":"trimesterList"}, globalData)
    
#changes a trimester start date to a different date (UNTESTED)
def changeTrimester(oldDate,newDate):
    oldTime = getUnixTime(oldDate)
    newTime = getUnixTime(newDate)

    current = db.globals.find({"name":"trimesters"})[0]
    current["value"].remove(oldTime)
    current["value"].append(newTime)

    for user in db.users.find({"isTutor":True}):
        if oldTime in user["credits"]:
            user["credits"][newTime] = user["credits"][oldTime]
            del user["credits"][oldTime]
            db.users.update({"username":user["username"]},user)
    db.globals.update({"name":"trimesters"},current)

#takes a string in the mm-dd-yyyy format and converts it to unix time
def getUnixTime(date):
    return int(time.mktime(datetime.datetime.strptime(date, "%m-%d-%Y").timetuple()))

#takes a unix time and converts it to a string in the mm-dd-yyyy format
def getDate(unixTime):
    return datetime.datetime.fromtimestamp(int(unixTime)).strftime('%m-%d-%Y')

#adds credits to a user dict given the date and the number of credits for the session
def addCredits(tutor,date,numCredits):
    taimu = getUnixTime(date)
    current = int(time.time())
    if current - taimu > twoWeeks:
        return False
    trimesterList = getTrimesterList()
    occurance = trimesterList[0]
    for trimester in trimesterList:
        if taimu >= trimester:
            occurance = trimester
    if occurance in tutor["credits"]:
        tutor["credits"][occurance] += numCredits
    else:
        tutor["credits"][occurance] = numCredits
    return True
"""
db.globals.remove({})
initializeTrimesters("05-05-2016","06-05-2016")
print getTrimesterList()
user = getUser("Jion")
 
print addCredits(user,"05-05-2016",1)
print user["credits"]

print addCredits(user,"06-01-2016",1)
print user["credits"]

changeTrimester("05-05-2016","05-06-2016")
changeTrimester("06-05-2016","06-06-2016")

print addCredits(user,"06-08-2016",1)
print user["credits"]

print addCredits(user,"05-25-2016",1)
print user["credits"]

print addCredits(user,"05-26-2016",1)
print user["credits"]"""
