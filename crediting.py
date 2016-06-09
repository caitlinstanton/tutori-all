from security import *
import time
import datetime

twoWeeks = 15 * 86400

def initializeTrimesters(trimester1,trimester2):
    db.globals.insert({"name":"trimesters", 
                       "value":[getUnixTime(trimester1),getUnixTime(trimester2)] })
def getTrimesterList():
    return db.globals.find({"name":"trimesters"})[0]["value"]

def addTrimester(date):
    globalData = db.globals.find({"name":"trimesters"})[0]
    trimesterList = getTrimesterList()
    trimesterList.append(getUnixTime(date))
    globalData["value"] = trimesterList
    db.globals.update({"name":"trimesterList"}, globalData)
    
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

def getUnixTime(date):
    return time.mktime(datetime.datetime.strptime(date, "%m-%d-%Y").timetuple())

def getDate(unixTime):
    return datetime.datetime.fromtimestamp(int(unixTime)).strftime('%m-%d-%Y')

def addCredits(tutor,date,numCredits):
    time = getUnixTime(date)
    current = int(time.time())
    if current - time > twoWeeks:
        return False
    trimesterList = getTrimesterList()
    occurance = trimesterList[0]
    for trimester in trimesterList:
        if time >= trimester:
            occurence = trimester
            break
    if occurance in tutor["credits"]:
        tutor["credits"][occurance] += numCredits
    else:
        tutor["credits"][occurance] = numCredits
    return True
