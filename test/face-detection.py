import sys
sys.path.append("../")

import cv2
from detection.face_matching import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import json


def match_with_database(img, database):
    
    faces = detect_faces(img)

    for face in faces:
        try:
            
            aligned_face = align_face(img, face)

            
            embedding = extract_features(aligned_face)

            embedding = embedding[0]["embedding"]

            
            match = match_face(embedding, database)

            if match is not None:
                print(f"Match found: {match}")
            else:
                print("No match found")
        except:
            print("No face detected")
        

    
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)
        print("Face detected")

    
    cv2.imshow("Detected Faces", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


cred_json = os.environ["FIREBASE_CREDENTIALS_JSON"]
cred_info = json.loads(cred_json)
cred = credentials.Certificate(cred_info)
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://face-recognition-486cb-default-rtdb.firebaseio.com/",
    },
)


ref = db.reference("Students")

number_student = len(ref.get())
print("There are", (number_student - 1), "students in the database")

database = {}
for i in range(1, number_student):
    studentInfo = db.reference(f"Students/{i}").get()
    studentName = studentInfo["name"]
    studentEmbedding = studentInfo["embeddings"]
    database[studentName] = studentEmbedding


camera_or_image = input("Enter (1) if you have camera\nEnter (2) if you have image: ")

if camera_or_image == "1":
    
    vid = cv2.VideoCapture(0)
    while True:
        
        
        ret, frame = vid.read()

        
        cv2.putText(
            frame,
            "Press 's' to save the image",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

        
        cv2.imshow("frame", frame)

        
        
        
        if cv2.waitKey(1) & 0xFF == ord("s"):
            break
    
    vid.release()
    
    cv2.destroyAllWindows()

    faces = match_with_database(frame, database)


elif camera_or_image == "2":
    
    img = cv2.imread("../examples/face1.png")
    faces = match_with_database(img, database)
