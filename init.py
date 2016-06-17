from sessions import *
from crediting import *
db.users.remove({})
db.sessions.remove({})

print "please select and admin password:"
password = raw_input()
createAccount("admin@gmail.com",password,"n/a","n/a","admin","admin")
changeValue("admin@gmail.com","isAdmin",True)
changeValue("admin@gmail.com","isVerified",True)
print "you can use this password with the email 'admin@gmail.com' to log in"
print "choose the start date of the last trimester (mm-dd-yyyy):"
last = raw_input()
print "choose the start date of the current trimester (mm-dd-yyyy):"
current = raw_input()
initializeTrimesters(last,current)
