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
- [Dependencies](#dependencies)
- [Future Improvements](#future-improvements)
- [Contribution](#contribution)
- [Troubleshooting & Compatibility Fixes](#troubleshooting--compatibility-fixes)
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

3. **Configure Firebase & Cloudinary**:
   - Set up Firebase for the real-time database.
   - Sign up for [Cloudinary](https://cloudinary.com/) and obtain your **Cloud name**, **API key**, and **API secret**.
   - Update `configs/database.yaml` with Firebase details and your Cloudinary credentials.
   - Place your Firebase service account key (JSON) at the path specified in the YAML file.

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

## Dependencies

The key dependencies include:

- **Flask** (3.1.1)
- **OpenCV**
- **Firebase Admin SDK**
- **Werkzeug**
- **DeepFace**
- **Dlib**
- **PyYAML**

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

## Troubleshooting & Compatibility Fixes

Due to legacy versions of Flask and Firebase Admin SDK, some compatibility issues may occur when using newer Python environments. Below are manual patches required to make the system work without upgrading dependencies:

### 🔧 Flask & Jinja2 Compatibility

**Problem**: Import errors for `escape` and `Markup`.

**Fix**: In the following files, replace `from jinja2 import Markup` with `from markupsafe import Markup` and similarly for `escape`.

**Files to patch**:

- `venv/Lib/site-packages/flask/__init__.py`
- `venv/Lib/site-packages/flask/json/__init__.py`
- `venv/Lib/site-packages/flask/json/tag.py`

---

### 🔧 Firebase SDK Retry Issue

**Problem**: `method_whitelist` is no longer valid in `urllib3`.

**Fix**: In:
- `venv/Lib/site-packages/firebase_admin/_http_client.py`

Replace:
```python
method_whitelist=_ANY_METHOD
```
With:
```python
allowed_methods=_ANY_METHOD
```

---

### 📁 shape_predictor_68_face_landmarks.dat Required

1. Download from:  
   [https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2](https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2)

2. Extract it and move the `.dat` file to:  
   `detection/shape_predictor_68_face_landmarks.dat`

3. Your `face_matching.py` should use:
```python
datFile = os.path.join(os.path.dirname(__file__), 'shape_predictor_68_face_landmarks.dat')
```

---

### 🔐 Firebase Service Account Key Missing

1. Go to Firebase Console → Project Settings → Service Accounts.
2. Click “Generate New Private Key”.
3. Save the `.json` file in your `configs/` folder.
4. Update the YAML config to point to that file:
```yaml
firebase:
  pathToServiceAccount: "configs/serviceAccountKey.json"
```

---

### 🖼️ Cloudinary Credentials Missing

1. Create a free account at [Cloudinary](https://cloudinary.com/).
2. Navigate to the **Dashboard** to find your *Cloud name*, *API key*, and *API secret*.
3. Edit `configs/database.yaml` and fill in these values under the `cloudinary` section:
   ```yaml
   cloudinary:
     cloud_name: "your_cloud_name"
     api_key: "your_api_key"
     api_secret: "your_api_secret"
   ```

---

### 📦 PyYAML Not Found

If you see `ModuleNotFoundError: No module named 'yaml'`, install it using:

```bash
pip install PyYAML
```

---

## License

[MIT License](LICENSE)

---

## Technical Information

- Python 3.11
- TensorFlow 2.19.0
- Flask 3.1.1
- Firebase Admin SDK 6.9.0
- DeepFace 0.0.93
- OpenCV 4.11.0.86
- Dlib 19.24.0

---

## Author

**Tavish Chawla**  
📧 [tchawla827@gmail.com](mailto:tchawla827@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/tavish-chawla-3b1673278/)