from flask import (
    Flask,
    render_template,
    get_flashed_messages,
    request,
    redirect,
    url_for,
    Response,
    flash,
    jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import numpy as np
from flask_cors import CORS
from jinja2 import select_autoescape, FileSystemLoader

import os
import cv2
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import cloudinary
from detection.face_matching import detect_faces, align_face, extract_features, match_face, identify_face
from utils.configuration import load_yaml

from jinja2 import Environment, select_autoescape


config_file_path = load_yaml("configs/database.yaml")

TEACHER_PASSWORD_HASH = config_file_path["teacher"]["password_hash"]

cred = credentials.Certificate(config_file_path["firebase"]["pathToServiceAccount"])
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": config_file_path["firebase"]["databaseURL"],
    },
)

cloudinary.config(
    cloud_name=config_file_path["cloudinary"]["cloud_name"],
    api_key=config_file_path["cloudinary"]["api_key"],
    api_secret=config_file_path["cloudinary"]["api_secret"],
)


def upload_database(filename):
    """
    Checks if a file with the given filename already exists in the
    database storage, and if not, uploads the file to the database.
    """
    valid = False

    try:
        cloudinary.api.resource(filename)
        valid = True
        error = f"<h1>{filename} already exists in the database</h1>"
    except cloudinary.exceptions.NotFound:
        pass

    if not filename[:-4].isdigit():
        valid = True
        error = f"<h1>Please make sure that the name of the {filename} is a number</h1>"

    if not valid:

        filename = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        cloudinary.uploader.upload(filename, public_id=os.path.basename(filename))
        error = None

    return valid, error


def match_with_database(img, database):
    """The function "match_with_database" takes an image and a database as input, detects faces in the
    image, aligns and extracts features from each face, and matches the face to a face in the database.
    """
    global match

    faces = detect_faces(img)

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)

    cv2.imwrite("static/recognized/recognized.png", img)

    for face in faces:
        try:

            aligned_face = align_face(img, face)

            embedding = extract_features(aligned_face)

            embedding = embedding[0]["embedding"]

            match = match_face(embedding, database)

            if match is not None:
                return f"Match found: {match}"
            else:
                return "No match found"
        except:
            return "No face detected"


app = Flask(__name__, template_folder="template", static_folder="static")

CORS(app)

app.jinja_env = Environment(
    loader=FileSystemLoader("template"), autoescape=select_autoescape(["html", "xml"])
)
app.jinja_env.globals.update(url_for=url_for)
app.secret_key = "123456"


UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def login():
    return render_template(
        "student_login.html", get_flashed_messages=get_flashed_messages
    )

@app.route("/logout")
def logout():
    return render_template(
        "student_login.html", get_flashed_messages=get_flashed_messages
    )

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/try")
def test():
    return render_template("try.html")  # Create a basic test.html template to test url_for


@app.route("/add_info")
def add_info():
    return render_template("add_info.html")


@app.route("/teacher_login", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        teacher_name = request.form.get("teacher_name")
        password = request.form.get("password")

        if teacher_name == "admin" and check_password_hash(TEACHER_PASSWORD_HASH, password):
            return redirect(url_for("home"))
        else:
            flash("Incorrect credentials")

        return render_template(
            "teacher_login.html", get_flashed_messages=get_flashed_messages
        )

    return render_template("teacher_login.html")


@app.route("/upload", methods=["POST"])
def upload():
    global filename

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        ref = db.reference("Students")
        try:

            studentId = len(ref.get())
        except TypeError:
            studentId = 1

        filename = f"{studentId}.png"

        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        val, err = upload_database(filename)

        if val:
            return err

        return redirect(url_for("add_info"))

    return "File upload failed", 400


def allowed_file(filename):

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    url = url_for("static", filename="images/" + filename, v=timestamp)

    return f'<h1>File uploaded successfully</h1><img src="{url}" alt="Uploaded image">'


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")



@app.route("/markin", methods=["POST"])
def markin():
    global filename, detection
    ret, frame = video.read()

    if ret:
        out_students_ref = db.reference("Out Students")
        students_data = db.reference("Students").get()

        print("All students data:", students_data)

        database = {}
        # Handling both list and dict types for students data
        if isinstance(students_data, list):
            for studentInfo in students_data:
                if studentInfo:
                    studentName = studentInfo.get("name")
                    studentEmbedding = studentInfo.get("embeddings")
                    if studentName and studentEmbedding:
                        database[studentName] = studentEmbedding
        elif isinstance(students_data, dict):
            for student_id, studentInfo in students_data.items():
                if studentInfo:
                    studentName = studentInfo.get("name")
                    studentEmbedding = studentInfo.get("embeddings")
                    if studentName and studentEmbedding:
                        database[studentName] = studentEmbedding

        detection = match_with_database(frame, database)

        if detection and "Match found" in detection:
            student_name = detection.split(": ")[-1]
            print(f"Detected student: {student_name}")

            # Check if the student is marked out in 'Out Students'
            if out_students_ref.child(student_name).get() is not None:
                # Remove the student from 'Out Students' (they are marked in now)
                out_students_ref.child(student_name).delete()
                print(f"{student_name} has been marked in and removed from 'Out Students'.")

                # Update the history with time_in information
                history_ref = db.reference("History")
                history_entries = history_ref.order_by_child("name").equal_to(student_name).get()

                if history_entries:
                    # Convert to a list and find the latest entry
                    entries = list(history_entries.values())
                    latest_entry = max(entries, key=lambda x: x["time_out"])  # Find the latest entry

                    # Get the key of the latest entry
                    latest_entry_key = next(key for key, value in history_entries.items() if value == latest_entry)

                    # Update the time_in for the latest entry
                    history_ref.child(latest_entry_key).update({"time_in": str(datetime.now())})
                    print(f"Updated history for {student_name} with time_in.")

                return {
                    "status": "success",
                    "message": f"{student_name} has been marked in successfully!",
                }, 200
            else:
                print(f"{student_name} is not marked out.")
                return {
                    "status": "error",
                    "message": f"{student_name} is not currently marked out.",
                }, 400
        else:
            print("No matching student found.")
            return {"status": "error", "message": "No matching student found."}, 400

    print("Error capturing image.")
    return {"status": "error", "message": "Error capturing image"}, 500




@app.route("/markout", methods=["POST"])
def markout():
    global filename, detection
    ret, frame = video.read()

    if ret:
        ref = db.reference("Students")
        students_data = ref.get()

        # Count the number of students in the database
        if isinstance(students_data, dict):
            number_student = len(students_data)
        elif isinstance(students_data, list):
            number_student = len(students_data)
        else:
            number_student = 0

        print("There are", number_student, "students in the database")

        database = {}
        if isinstance(students_data, dict):
            for student_id, studentInfo in students_data.items():
                if studentInfo:
                    studentName = studentInfo.get("name")
                    studentEmbedding = studentInfo.get("embeddings")
                    if studentName and studentEmbedding:
                        database[studentName] = studentEmbedding
        elif isinstance(students_data, list):
            for studentInfo in students_data:
                if studentInfo:
                    studentName = studentInfo.get("name")
                    studentEmbedding = studentInfo.get("embeddings")
                    if studentName and studentEmbedding:
                        database[studentName] = studentEmbedding

        detection = match_with_database(frame, database)

        if detection and "Match found" in detection:
            student_name = detection.split(": ")[-1]
            print(f"Detected student: {student_name}")

            rollNumber = None
            student_class = None
            phoneNumber = None  # Add this for phone number

            # Get student details including phone number
            if isinstance(students_data, dict):
                for student_id, studentInfo in students_data.items():
                    if studentInfo and studentInfo["name"] == student_name:
                        rollNumber = studentInfo.get("rollNumber", "Not Provided")
                        student_class = studentInfo.get("classes", "Not Provided")
                        phoneNumber = studentInfo.get("phone", "Not Provided")  # Get phone number
                        print(f"Found rollNumber: {rollNumber}, class: {student_class}, phone: {phoneNumber}")
                        break
            elif isinstance(students_data, list):
                for studentInfo in students_data:
                    if studentInfo and studentInfo["name"] == student_name:
                        rollNumber = studentInfo.get("rollNumber", "Not Provided")
                        student_class = studentInfo.get("classes", "Not Provided")
                        phoneNumber = studentInfo.get("phone", "Not Provided")  # Get phone number
                        print(f"Found rollNumber: {rollNumber}, class: {student_class}, phone: {phoneNumber}")
                        break

            if rollNumber == "Not Provided" or student_class == "Not Provided":
                if rollNumber == "Not Provided":
                    print("Roll number is missing.")
                if student_class == "Not Provided":
                    print("Class is missing.")
                return "Student info incomplete", 500

            requests_ref = db.reference("Outpass Requests")
            approved_requests = (
                requests_ref.order_by_child("rollNumber").equal_to(rollNumber).get()
            )

            current_date = datetime.now().date().isoformat()
            has_approved_request = False
            approved_request_key = None

            if approved_requests:
                for request_key, request in approved_requests.items():
                    if (
                        request.get("status") == "Approved"
                        and request.get("outgoing_date") == current_date
                    ):
                        has_approved_request = True
                        approved_request_key = request_key
                        break

            if not has_approved_request:
                return {
                    "status": "error",
                    "message": "No approved outpass request found for today.",
                }, 403

            out_students_ref = db.reference("Out Students")

            if out_students_ref.child(student_name).get() is not None:
                return {
                    "status": "error",
                    "message": f"{student_name} is already marked out.",
                }, 400

            try:
                student_count = (
                    len(out_students_ref.get()) if out_students_ref.get() else 0
                )
            except TypeError:
                student_count = 0

            filename = f"{student_count}.png"
            cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], filename), frame)

            # Mark student as out and store in 'Out Students'
            out_students_ref.child(student_name).set(
                {
                    "name": student_name,
                    "rollNumber": rollNumber,
                    "class": student_class,
                    "phone": phoneNumber,  # Store phone number
                    "time_out": str(datetime.now()),
                    "image_filename": filename,
                }
            )

            # Update the outpass request status to 'Expired'
            if approved_request_key:
                requests_ref.child(approved_request_key).update({"status": "Expired"})

            # Store in 'History' for record keeping
            history_ref = db.reference("History")
            history_ref.push(
                {
                    "name": student_name,
                    "rollNumber": rollNumber,
                    "phone": phoneNumber,  # Include phone number in history
                    "time_out": str(datetime.now()),
                    "time_in": None,  # Will update this when marking in
                }
            )

            print("Successfully added student to 'Out Students' and 'History'.")
            return {
                "status": "success",
                "message": f"{student_name} (Roll No: {rollNumber}) marked out successfully!",
            }, 200

        else:
            print("No matching student found or no face detected.")
            return {
                "status": "error",
                "message": "No face detected or student not recognized.",
            }, 404

    print("Error capturing image.")
    return {"status": "error", "message": "Error capturing image"}, 500





@app.route("/capture", methods=["POST"])
def capture():
    global filename
    ret, frame = video.read()
    if ret:

        ref = db.reference("Students")

        try:

            studentId = len(ref.get())

        except TypeError:
            studentId = 1

        filename = f"{studentId}.png"

        cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], filename), frame)

        val, err = upload_database(filename)

        if val:
            return err

    return redirect(url_for("add_info"))


@app.route("/success/<filename>")
def success(filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    url = url_for("static", filename="images/" + filename, v=timestamp)

    return f'<h1>{filename} image uploaded successfully to the database</h1><img src="{url}" alt="Uploaded image">'


@app.route("/submit_info", methods=["POST"])
def submit_info():

    name = request.form.get("name")
    rollNumber = request.form.get("rollNumber")
    email = request.form.get("email")
    phone = request.form.get("phone")
    userType = request.form.get("userType")
    hostel = request.form.get("classes")
    password = request.form.get("password")
    hashed_password = generate_password_hash(password)

    studentId, _ = os.path.splitext(filename)
    fileName = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    data = cv2.imread(fileName)

    faces = detect_faces(data)

    for face in faces:
        aligned_face = align_face(data, face)
        embedding = extract_features(aligned_face)
        break

    ref = db.reference("Students")
    student_data = {
        str(studentId): {
            "name": name,
            "rollNumber": rollNumber,
            "email": email,
            "phone": phone,
            "userType": userType,
            "classes": hostel,
            "password": hashed_password,
            "embeddings": embedding[0]["embedding"],
        }
    }

    for key, value in student_data.items():
        ref.child(key).set(value)

    return redirect(url_for("success", filename=filename))


@app.route("/recognize", methods=["GET", "POST"])
def recognize():
    global detection
    ret, frame = video.read()
    if ret:

        ref = db.reference("Students")

        number_student = len(ref.get())
        print("There are", (number_student - 1), "students in the database")

        database = {}
        for i in range(1, number_student):
            studentInfo = db.reference(f"Students/{i}").get()
            studentName = studentInfo["name"]
            studentEmbedding = studentInfo["embeddings"]
            database[studentName] = studentEmbedding

        detection = match_with_database(frame, database)

    return redirect(url_for("select_class"))


@app.route("/select_class", methods=["GET", "POST"])
def select_class():
    if request.method == "POST":

        selected_class = request.form.get("classes")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        url = url_for("static", filename="recognized/recognized.png", v=timestamp)

        ref = db.reference("Students")

        number_student = len(ref.get())

        for i in range(1, number_student + 1):
            studentInfo = db.reference(f"Students/{i}").get()
            if match == studentInfo["name"]:

                print(studentInfo["classes"])
                if selected_class == studentInfo["classes"]:

                    current_attendance = studentInfo.get("attendance", {}).get(
                        selected_class, 0
                    )
                    ref.child(f"{i}/attendance/{selected_class}").set(
                        current_attendance + 1
                    )

                    return f'<h2>Selected Class: {selected_class} - {detection}</h2><img src="{url}" alt="Recognized face">'
                else:
                    return f'<h2>Student not in class - {detection}</h2><img src="{url}" alt="Recognized face">'
    else:

        return render_template("select_class.html")


@app.route("/student_login", methods=["POST"])
def student_login():
    student_id = request.form.get("rollNumber")
    password = request.form.get("password")

    ref = db.reference("Students")
    students_info = ref.get()

    matching_student = None

    if isinstance(students_info, list):
        for student in students_info:
            if student is not None:
                if student.get("rollNumber") == student_id:
                    matching_student = student
                    break

    if matching_student:
        if check_password_hash(matching_student["password"], password):
            return redirect(url_for("student_dashboard", roll_number=student_id))
        else:
            flash("Incorrect password")
    else:
        flash("Student ID not found")

    return render_template(
        "student_login.html", get_flashed_messages=get_flashed_messages
    )


@app.route("/student_dashboard/<roll_number>")
def student_dashboard(roll_number):

    ref = db.reference("Students")
    student_info = ref.order_by_child("rollNumber").equal_to(roll_number).get()

    if not student_info:
        return "Student not found", 404

    student = next(iter(student_info.values()))

    requests_ref = db.reference("Outpass Requests")

    requests = requests_ref.order_by_child("rollNumber").equal_to(roll_number).get()

    request_list = []
    if requests:
        for key, value in requests.items():
            request_list.append(value)

    return render_template(
        "student_dashboard.html", student=student, requests=request_list
    )


@app.route("/mark_out")
def mark_out():
    return render_template("mark_out.html")


@app.route("/mark_in")
def mark_in():
    return render_template("mark_in.html")


@app.route("/view_out_students")
def view_out_students():
    try:

        out_students_ref = db.reference("Out Students")

        out_students = out_students_ref.get()

        if out_students is None:
            out_students = {}

        return render_template("view_out_students.html", out_students=out_students)
    except Exception as e:

        return f"An error occurred: {str(e)}"


@app.route("/submit_outpass_request", methods=["POST"])
def submit_outpass_request():
    name = request.form.get("name")
    roll_number = request.form.get("rollNumber")
    outgoing_date = request.form.get("outgoing_date")
    outgoing_time = request.form.get("outgoing_time")
    ingoing_date = request.form.get("ingoing_date")
    ingoing_time = request.form.get("ingoing_time")
    reason = request.form.get("reason")

    outpass_request_ref = db.reference("Outpass Requests")
    outpass_request_ref.push(
        {
            "name": name,
            "rollNumber": roll_number,
            "outgoing_date": outgoing_date,
            "outgoing_time": outgoing_time,
            "ingoing_date": ingoing_date,
            "ingoing_time": ingoing_time,
            "reason": reason,
            "status": "Pending",
        }
    )

    return redirect(url_for("student_dashboard", roll_number=roll_number))


def gen_frames():
    global video
    video = cv2.VideoCapture(0)
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/admin_review")
def admin_review():
    outpass_requests_ref = db.reference("Outpass Requests")
    outpass_requests = outpass_requests_ref.get()

    request_list = []
    if outpass_requests:
        for key, value in outpass_requests.items():
            value["id"] = key
            # Convert outgoing_date to a datetime object for sorting, if present
            if "outgoing_date" in value:
                value["outgoing_datetime"] = datetime.strptime(value["outgoing_date"], "%Y-%m-%d")
            else:
                value["outgoing_datetime"] = datetime.max  # Use a max date if not present
            request_list.append(value)

    # Sort by status ('Pending' first) and then by outgoing date (earliest date first)
    request_list.sort(
        key=lambda x: (x["status"] != "Pending", x["outgoing_datetime"])
    )

    # Remove the temporary outgoing_datetime key after sorting
    for request in request_list:
        request.pop("outgoing_datetime", None)

    return render_template("admin_review.html", requests=request_list)


@app.route("/update_request_status", methods=["POST"])
def update_request_status():
    request_id = request.form.get("id")
    status = request.form.get("status")

    request_ref = db.reference(f"Outpass Requests/{request_id}")
    request_ref.update({"status": status})

    return redirect(url_for("admin_review"))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/view_history")
def view_history():
    history_ref = db.reference("History")
    history_data = history_ref.get()  # Fetch data from Firebase

    if history_data is None:
        history_data = {}  # Initialize as an empty dictionary if no history

    return render_template("view_history.html", history=history_data)
@app.post("/api/frame")
def api_frame():
    data = request.data
    if not data:
        return jsonify({"error": "no image"}), 400
    frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    students_data = db.reference("Students").get()
    database = {}
    if isinstance(students_data, dict):
        iterable = students_data.values()
    else:
        iterable = students_data or []
    for info in iterable:
        if info:
            name = info.get("name")
            emb = info.get("embeddings")
            if name and emb:
                database[name] = emb
    name, prob = identify_face(frame, database)
    return jsonify({"name": name, "probability": prob})




if __name__ == "__main__":
    app.run(debug=True)
