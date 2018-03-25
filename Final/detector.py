import cv2,os
import numpy as np
from PIL import Image 
import pickle
import argparse
import MySQLdb

found=False
def insert(passed_reg_no,name,attendance):
    print '\n\nupdating....'
    db = MySQLdb.connect("localhost","root","root","attendance_System" )
    cursor = db.cursor()

    attendance=attendance+1
    try:
       cursor.execute("UPDATE attendance_sheet SET ATTENDANCE = %s WHERE REG_NO=%s"%(attendance,passed_reg_no))
        
      # cursor.execute("INSERT INTO attendance_sheet(REG_NO,NAME, STATUS, SUBJECT, TIME)\
       #      VALUES (%s, %s, 'PRESENT', '<Future Work>', NOW())",(passed_reg_no,name))

       db.commit()
       print('attendance_sheet is updated')
    except:
       db.rollback()
       print 'couldnt insert into DATABASE\n'

    db.close()


def check(passed_reg_no):
    db = MySQLdb.connect("localhost","root","root","attendance_System" )
    cursor = db.cursor()
    print '\nchecking  ',passed_reg_no,' in the database'

    try:
       # cursor.execute("SELECT NAME FROM attendance_sheet WHERE REG_NO=%d",(passed_reg_no))

       cursor.execute("SELECT * FROM attendance_sheet WHERE REG_NO=280")
       results = cursor.fetchall()
       for row in results:
        name = row[1]
        attendance = row[3]
        print 'Name found in the DB = ',name
        insert(passed_reg_no,name,attendance)
        found = True
    except:
       print "Error: unable to fecth data\n\n"
    db.close()    


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, required="true", help="path to input video file")
args = vars(ap.parse_args())

recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('trainer/trainer.yml')
cascadePath = "Classifiers/face.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

video_source = args['video']
print video_source
cam = cv2.VideoCapture(video_source)
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1) 

print('\n-------RECOGNISING THE FACE------\n')

ret, im =cam.read()
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
for(x,y,w,h) in faces:
    nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
    cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
 
    cv2.cv.PutText(cv2.cv.fromarray(im),str(nbr_predicted)+"--"+str(conf), (x,y+h),font, 255) 

    imS = cv2.resize(im,(960, 540))                  
    cv2.imshow("output", imS) 
    cv2.waitKey(10)
    print'recognizer predicted ',nbr_predicted,'\n'
    check(nbr_predicted)
    
    if(found==True):
        print("Attendance is updated for jitu\n\n")
        












