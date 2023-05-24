# Encoding part,this will be done only once
import os
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("Service_account_key.json")
firebase_admin.initialize_app(cred,{
    "databaseURL": "https://face-authentication-3f1dc-default-rtdb.firebaseio.com/",
    "storageBucket": "face-authentication-3f1dc.appspot.com"
})

# importing all the images(faces)
folderImagePath= 'Images'
modePathList= os.listdir((folderImagePath))
# print(modePathList)
# saving the images in list (imageList)
imageList = []

# saving student ID's
studentID = []
for path in modePathList:
    imageList.append(cv2.imread(os.path.join(folderImagePath,path)))

    # getting the student id using os.splitext() to removing the file extension
    studentID.append(os.path.splitext(path)[0])

    # Uploading the images to the data base.
    print("Uploading images started....")
    filename =f'{folderImagePath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    print("Uploaded images successfully")

    # to understand the process
    print(os.path.splitext(path))

# print(len(imageList))
# print(studentID)

# the encoding method
def FindEncoding(imgList):
    encoded_img=[]
    for img in imgList:
        # converting images from BGR to RGB(cv2 use RGB but face_recognition use BGR)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode= face_recognition.face_encodings(img)[0]
        encoded_img.append(encode)
    return encoded_img

print("Encoding started.....")
encoded_img_list=FindEncoding(imageList)
# print(encoded_img_list)
print("Encoded.")
# storing the encoded image and stu id in a file using pickle
print("Started file saving...")
encoded_img_list_with_IDs= [encoded_img_list,studentID]
file = open("Encodefile.p",'wb')
pickle.dump(encoded_img_list_with_IDs,file)
file.close()
print('file saved')