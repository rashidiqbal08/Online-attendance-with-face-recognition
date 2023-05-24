import pickle
import cv2
import os
import cvzone
import face_recognition
import numpy as np
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from firebase_admin import storage
cred = credentials.Certificate("Service_account_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL":"https://face-authentication-3f1dc-default-rtdb.firebaseio.com/",
    "storageBucket":"face-authentication-3f1dc.appspot.com"
})

# creating the bucket for storing the image from database
# bucket = storage.bucket()

# STAGE 1-  WEBCAM
cap = cv2.VideoCapture(0)
cap.set(4, 800)
cap.set(3, 400)
imgBackground = cv2.imread("Resources/background.png")

# importing the modes images
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
print(modePathList)
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
print(len(imgModeList))

# loading the encoded file
file = open('Encodefile.p', 'rb')
encoded_img_list_with_IDs = pickle.load(file)
encoded_img_list, studentID = encoded_img_list_with_IDs
# print(studentID)
# print(len(encoded_img_list))
# print(len(studentID))
file.close()


modeType = 0
id = -1
counter = 0
imgStudent = []
while True:
    success, img = cap.read()
    # resizing the image
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # converting it from bgr to  rgb(It's important otherwise it won't work)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


    # comparing the current faces from encoded one.
    face_cur_frame = face_recognition.face_locations(imgS)
    encode_cur_frame = face_recognition.face_encodings(imgS, face_cur_frame)
    # overlaying the graphics
    imgBackground[162:162 + 480, 55:55 + 640] = img
    # Adding the active mode graphics
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    if face_cur_frame:

        for encode_face, faceLoc in zip(encode_cur_frame,face_cur_frame):
            # matching the live images with encoded image.
            matches = face_recognition.compare_faces(encoded_img_list,encode_face)
            face_dist = face_recognition.face_distance(encoded_img_list,encode_face)
            # print("matches: ", matches)
            # print("face_distance: ", face_dist)

            # indexing the face dist for comparing
            matchIndex = np.argmin(face_dist)
            # print("Match_index: ", matchIndex)]

            # if match index is true that means known face detected.
            if matches[matchIndex]:
                print("Known face detected. ")
                print("Enrollment No. :", studentID[matchIndex], "PRESENT")

                # # creating the rectangular box
                # y1, x2, y2, x1 = faceLoc
                # y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                # bbox = 55+x1, 162+y1, x2-x1, y2-y1
                # imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                # module(8) 'getting user data' part running
                id = studentID[matchIndex]
                if counter == 0:
                    counter = 1
                    modeType = 1
            if counter != 0:
                if counter == 1:
                    # get the data
                    student_info = db.reference(f'Students/{id}').get()
                    print("Student information from database: ", student_info)
                    # # get the images (for now it's not working)
                    # blob = bucket.get_blob(f'Images/{id}.png')
                    # # creating an array (standard method of converting)
                    # array = np.frombuffer(blob.download_as_string(), np.uint8)
                    # # converting from bgr to rgb
                    # imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)


                    ## update data of attendance (day increment)


                    # applying the timer for attendance (limit)
                    datetimeObject = datetime.strptime(student_info['Last attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    #updating into the database
                    # creating the reference
                    if secondsElapsed > 30:

                        ref = db.reference(f'Students/{id}')
                        student_info['total attendance'] += 1
                        ref.child('total attendance').set(student_info['total attendance'])
                        ref.child('Last attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        counter = 0
                #here we are changing the modes accordingly
                if modeType != 3:

                    if 10<counter <=20:
                        modeType = 2
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    if counter <= 10:

                        # here we are putting the information into the graphics
                        cv2.putText(imgBackground, str(student_info['total attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(student_info['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (50, 50, 50), 1),
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (50, 50, 50), 1)

                        # displaying the image into graphics
                        #for now displaying image is not working.
                        # imgBackground[175:175+650, 909:909+562] = imgStudent
                    counter += 1
                    if counter >=20:
                        counter = 0
                        modeType = 0
                        student_info = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow('Face Attendance', imgBackground)
    cv2.waitKey(1)

# Face detection part (here we'll import the encoded file and check if recognized face is known or not)


