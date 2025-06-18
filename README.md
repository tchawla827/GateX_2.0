# GateX Gate Outpass Management System

**GateX** is a facial recognition-based Gate Outpass Management System tailored for college campuses. Students can request outpasses, mark their departure and return using a facial recognition system, and track their request history. Admins manage approvals, view the status of currently out students, and access historical records.

This project, built with Python, Flask, OpenCV, and Firebase, streamlines gate management by replacing manual processes with automation, ensuring security and accuracy.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment on Render](#deployment-on-render)
- [Dependencies](#dependencies)
- [Future Improvements](#future-improvements)
- [Contribution](#contribution)
- [License](#license)
- [Technical Information](#technical-information)
- [Author](#author)

---

## Introduction

Manual gate management can be cumbersome, time-intensive, and error-prone. GateX leverages facial recognition to automate and secure the process. Students submit outpass requests, which admins approve or reject. Once approved, students can mark themselves out or back in with a facial recognition-based verification.

The system tracks student movements, maintains history logs, and ensures adherence to campus policies.

---

## Features

GateX offers the following features:

1. **Facial Recognition-Based Marking**:  
   Mark "out" and "in" times using advanced face recognition.

2. **Outpass Request System**:  
   Students can request permission for leaving the campus, providing required details like date, time, and reason.

3. **Admin Panel**:  
   Review and approve/reject requests.  
   View students currently out.  
   Access comprehensive history logs.

4. **Student Dashboard**:  
   Track request history.

5. **Data Integrity**:
   Firebase Realtime Database ensures instant data updates, while Cloudinary stores uploaded images securely.

6. **User Roles**:  
   Distinct functionalities for admins and students.

7. **Responsive Web Interface**:  
   A user-friendly interface built with Flask.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/tchawla827/GateX.git
   ```

2. **Set Up Environment**:
   - Create and activate a virtual environment.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
     The versions in `requirements.txt` are final. No additional monkey
     patches are required.

3. **Configure Firebase & Cloudinary**:
   - Set up Firebase for the real-time database.
   - Sign up for [Cloudinary](https://cloudinary.com/) and obtain your **Cloud name**, **API key**, and **API secret**.
  - Copy `configs/database.example.yaml` to `configs/database.yaml` and update it with your Firebase and Cloudinary credentials.
  - Place your Firebase service account key (JSON) at the path specified in the YAML file or use the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

4. **Download Face Landmark Model**:
   - Download: [shape_predictor_68_face_landmarks.dat.bz2](https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2)
   - Extract and place `shape_predictor_68_face_landmarks.dat` in the `detection/` folder.

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000`.

---

## Usage

### Students
- Submit outpass requests.
- Mark out/in using facial recognition.

### Admins
- Approve or reject outpass requests.
- Monitor current out status and view history.

---

## Deployment on Render

1. Ensure all project dependencies are installed with `pip install -r requirements.txt`.
2. Copy `configs/database.example.yaml` to `configs/database.yaml` and fill in your credentials.
3. Upload `shape_predictor_68_face_landmarks.dat` to the `detection/` folder.
4. Commit your code to a Git repository and connect it to [Render](https://render.com).
5. On Render, create a new **Web Service** and set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - Add environment variables for `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`,
     `CLOUDINARY_API_SECRET`, `GOOGLE_APPLICATION_CREDENTIALS`,
     `FIREBASE_DATABASE_URL`, `TEACHER_PASSWORD_HASH`, and optionally `CONFIG_PATH`.
6. Deploy the service. Render will automatically build and start the Flask app.

---

## Dependencies

The key dependencies include:


- **Flask** 3.x

- **OpenCV**
- **Firebase Admin SDK** 6.x
- **Werkzeug**
- **DeepFace**
- **Dlib**
- **PyYAML** (included in `requirements.txt`)

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Future Improvements

- Enhanced UI for a modern user experience.
- Real-time notifications for approvals.
- Deploying the system to a cloud platform for broader accessibility.

---

## Contribution

Contributions are welcome! Open an issue or submit a pull request for bug fixes, feature additions, or enhancements.

---

## License

[MIT License](LICENSE)

---

## Technical Information


- Python 3.11.0
- TensorFlow 2.19.0
- Flask 3.x
- Firebase Admin SDK 6.x
- DeepFace 0.0.93
- OpenCV 4.11.0.86
- Dlib 20.0.0


---

## Author

**Tavish Chawla**  
📧 [tchawla827@gmail.com](mailto:tchawla827@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/tavish-chawla-3b1673278/)