import time
#import email seinding function
import smtplib
#imports code for generating emails
from email.mime.text import MIMEText



def log(user, message):
    try:
        logFile = open("logs/"+user+".txt","a")
        currentTime = time.strftime("%c")
        #print "time generated"
        logFile.write(currentTime+": "+message+"\n")
        logFile.close()
        return True
    except:
        return False

def email(user, subject, message):
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    
    s.login("stuyaristabot@gmail.com","stuy arista")


    message = MIMEText("message")
    message["Subject"] = subject
    sender = message["From"] = "stuyaristabot@gmail.com"
    recipient = message["To"] = "jijiglobe@yahoo.com"
    s.sendmail(sender, [recipient], message.as_string())
    
    s.quit()

email("jijiglobe@yahoo.com", "test", "more test")
