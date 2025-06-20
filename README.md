# GateX - Gate Outpass Management System

GateX automates student outpass management for college campuses using facial recognition. Students request permissions, mark their exit and entry with a camera, and administrators manage approvals and track history in real time.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Docker](#docker)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Future Improvements](#future-improvements)
- [Contribution](#contribution)
- [License](#license)
- [Technical Information](#technical-information)
- [Author](#author)

## Introduction
GateX replaces manual gate-book entries with a secure web application powered by Python, Flask, OpenCV and Firebase. Facial recognition ensures that only authorised students can mark themselves out or back in. Administrators have a full overview of current and past movements.

## Features
1. **Facial Recognition Based Marking** – mark "out" and "in" times using face recognition.
2. **Outpass Request System** – students submit requests with date, time and reason.
3. **Admin Panel** – approve or reject requests, view currently out students and access history.
4. **Student Dashboard** – track previous requests.
5. **Data Integrity** – Firebase Realtime Database for instant updates and Cloudinary for image storage.
6. **User Roles** – separate views for admins and students.
7. **Responsive Web Interface** – intuitive interface built with Flask and Tailwind CSS.

## Screenshots
Architecture and face detection diagrams are available in [`docs/images`](docs/images).

## Installation
1. **Clone the Repository**
```bash
git clone https://github.com/tchawla827/GateX.git
```
2. **Set Up Environment**
   - Ensure **Python 3.11** is installed.
   - Create a virtual environment and activate it:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
   - Install dependencies from the bundled wheelhouse so `dlib` does not compile:
```bash
pip install --upgrade pip
pip install --find-links wheelhouse -r requirements.txt
```
   - Generate a password hash for the teacher login if required:
```bash
python generate_password_hash.py
```
3. **Configure Firebase & Cloudinary**
   - Sign up for Firebase and Cloudinary and obtain credentials.
   - Copy `.env.example` to `.env` and populate `FIREBASE_CREDENTIALS_JSON`, `FIREBASE_DB_URL` and the Cloudinary variables. The `FIREBASE_CREDENTIALS_JSON` value should contain the entire service account JSON; escape newlines with `\n` when storing it.
4. **Download Face Landmark Model**
   - Download `shape_predictor_68_face_landmarks.dat.bz2` from the [dlib model repository](https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2).
   - Extract it to the `detection/` folder.
5. **DeepFace Weights from Hugging Face**
   - The first run downloads FaceNet weights from the Hugging Face Hub into `DEEPFACE_HOME` (defaults to `~/.deepface`). To pre-fetch them:
```bash
python - <<'PY'
from deepface.basemodels import Facenet
Facenet.loadModel()
PY
```
6. **Generate a Self-Signed Certificate**
   - Using [`mkcert`](https://github.com/FiloSottile/mkcert):
```bash
mkcert <your-host>
```
   - Rename or copy the generated certificate and key to `cert.pem` and `key.pem`, or create them with OpenSSL:
```bash
openssl req -newkey rsa:2048 -nodes -x509 -days 365 \
  -subj "/CN=<your-host>" \
  -keyout key.pem -out cert.pem
```
7. **Run the Application**
```bash
gunicorn -k eventlet -w 1 -b ${HOST:-0.0.0.0}:${PORT:-5000} app:app
```
Set `HOST` and `PORT` to control binding. When deploying publicly, use an HTTPS proxy such as Nginx or Caddy. These variables can also be stored in a `.env` file.

## Docker
Build and run GateX in a container:
```bash
docker build -t gatex .
docker run -p 5000:5000 \
  -e PORT=5000 -e HOST=0.0.0.0 gatex
```
The container starts the application with **Gunicorn** and the `eventlet` worker for WebSocket support. Customise the options via `docker-compose.yml` or a `.env` file.

## Usage
### Students
- Submit outpass requests.
- Mark out/in using facial recognition.

### Admins
- Approve or reject requests.
- Monitor current out status and view history.

## Dependencies
Key dependencies include:
- **Flask** 3.x
- **OpenCV**
- **Firebase Admin SDK** 6.x
- **Werkzeug**
- **DeepFace**
- **Dlib**
- **python-dotenv**
Install them with:
```bash
pip install -r requirements.txt
```

## Future Improvements
- Enhanced user interface.
- Real-time approval notifications.
- Deployment to a cloud platform for wider access.

## Contribution
Contributions are welcome—open an issue or submit a pull request for bug fixes or enhancements.

## License
[MIT License](LICENSE)

## Technical Information
- Python 3.11.0
- TensorFlow 2.19.0
- Flask 3.x
- Firebase Admin SDK 6.x
- DeepFace 0.0.93
- OpenCV 4.11.0.86
- Dlib 20.0.0

## Author
**Tavish Chawla**  
📧 [tchawla827@gmail.com](mailto:tchawla827@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/tavish-chawla-3b1673278/)
