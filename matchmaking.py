from security import *

def addGoodTeacher(username, 
    user = db.users.find({"username": username})
                   