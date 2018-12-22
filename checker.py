import time
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import smtplib
import email
import email.encoders 
import email.mime.text 
import email.mime.base
from email.mime.multipart import MIMEMultipart
from selenium.common.exceptions import NoSuchElementException

driver = wd.Chrome('''PATH FOR CHROME DRIVER''')
driver.get("https://lms.ashoka.edu.in/Contents/Grades/ViewGrades.aspx")

num = input("Number of Courses (including co-curriculars): ")

time.sleep(60)

courses = {}
subjects = []

for i in range (num):
    courses[i] = 0
    subjects.append(driver.find_element_by_id("ContentPlaceHolder1_lvView_lblCourseName_"+str(i)).text)

flag = 1

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("'''EMAIL'''", "'''PASSWORD'''")

while(flag):
    flag = 0
    for i in range(num):
        if courses[i] == 0:
            flag+=1
            try:
                grade = driver.find_element_by_id("ContentPlaceHolder1_lvView_lblGrades_"+str(i))
            except NoSuchElementException:
                continue
            html = "<p>Your "+ subjects[i] + " Grade is out.</p>"
            emailMsg = email.mime.multipart.MIMEMultipart('mixed')
            emailMsg['Subject'] = 'Grade Out'
            emailMsg['From'] = 'someText'
            emailMsg['To'] = 'yourEmail'
            emailMsg.attach(email.mime.text.MIMEText(html,'html'))
            server.sendmail("'''EMAIL'''","'''EMAIL'''",emailMsg.as_string())
            courses[i] = 1
    time.sleep(5)
    driver.refresh()
server.quit()