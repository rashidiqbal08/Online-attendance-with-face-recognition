
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("Service_account_key.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://face-authentication-3f1dc-default-rtdb.firebaseio.com/"
})

# creating a reference
reference= db.reference("Students")
data = {
    "321654":
        {
            "name": "Murtuza hasan",
            "major": "Robotics",
            "starting year": 2017,
            "total attendance": 6,
            "standing": "G",
            "year": 4,
            "Last attendance_time": "2022-12-11 00:54:34"
        },
    "AL201043":
        {
            "name": "Rashid Iqbal",
            "major": "CSE- AIML",
            "starting year": 2020,
            "total attendance": 0,
            "standing": "G",
            "year": 4,
            "Last attendance_time": "2022-12-11 00:54:34"
        },
    "AL201038":
        {
            "name": "Piyush Magarde",
            "major": "CSE- AIML",
            "starting year": 2020,
            "total attendance": 0,
            "standing": "G",
            "year": 4,
            "Last attendance_time": "2022-12-11 00:54:34"
        },
    "AL201026":
        {
            "name": "Jay Lowanshi",
            "major": "CSE- AIML",
            "starting year": 2020,
            "total attendance": 0,
            "standing": "G",
            "year": 4,
            "Last attendance_time": "2022-12-11 00:54:34"
        },
    "AL201034":
        {
            "name": "Mo Azhar",
            "major": "CSE- AIML",
            "starting year": 2020,
            "total attendance": 0,
            "standing": "G",
            "year": 4,
            "Last attendance_time": "2022-12-11 00:54:34"
        }
}
print("Started uploading database")
for key, value in data.items():
    reference.child(key).set(value)
print("Database uploaded")