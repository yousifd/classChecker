import urllib, json
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

send = False;
fromEmail = ""
toEmail = ""
password = ""

def email(body):
    msg = MIMEMultipart()
    msg["From"] = fromEmail
    msg["To"] = toEmail
    msg["Subject"] = "CLASSES OPEN"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(fromEmail, password)
    server.sendmail(fromEmail, toEmail, msg.as_string())
    server.quit()

message = ""
f = open("classes.txt", "r")
year = f.readline()
while(f != None):
    l = f.readline()
    if(not l):
        break
    major = l.split(" ")[0]
    numberOfClasses = l.split(" ")[1]
    for i in range(int(numberOfClasses)):
        line = f.readline()
        if(not line):
            break
        course = line.split(" ")[0]
        section = line.split(" ")[1]

        url = "http://web-app.usc.edu/web/soc/api/classes/" + major + "/" + year
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        for part in data:
          for c in data[part]["course"]:
            if(c["ScheduledCourseID"] == course):
              for sections in c["CourseData"]["SectionData"]:
                s = c["CourseData"]["SectionData"]
                for sect in s:
                  if(int(sect["id"]) == int(section)):
                    if(sect["spaces_available"] == sect["number_registered"]):
                      message += "Closed: " + course + " " + section + "\n"
                      send = True;
                    else:
                      message += "Open: " + course + " " + section + "\n"
                      send = True;
                    break
                break
          break


if(send):
    email(message)
