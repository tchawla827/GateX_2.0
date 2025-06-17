
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
- [License](#license)
- [Technical Information](#technical-information)

---

## Introduction

Manual gate management can be cumbersome, time-intensive, and error-prone. GateX leverages facial recognition to automate and secure the process. Students submit outpass requests, which admins approve or reject. Once approved, students can mark themselves out or back in with a facial recognition-based verification. 

The system tracks student movements, maintains history logs, and ensures adherence to campus policies.

---

## Features

GateX offers the following features:

1. **Facial Recognition-Based Marking**: 
   - Mark "out" and "in" times using advanced face recognition.
   
2. **Outpass Request System**: 
   - Students can request permission for leaving the campus, providing required details like date, time, and reason.

3. **Admin Panel**:
   - Review and approve/reject requests.
   - View students currently out.
   - Access comprehensive history logs.

4. **Student Dashboard**:
   - Track request history.

5. **Data Integrity**: 
   - Firebase integration ensures real-time and secure data storage.

6. **User Roles**: 
   - Distinct functionalities for admins and students.

7. **Responsive Web Interface**: 
   - A user-friendly interface built with Flask.

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

3. **Configure Firebase**:
   - Set up Firebase for real-time database and storage. Update the `configs/database.yaml` file with your project details (e.g., service account key path).

4. **Run the Application**:
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000`.

---

## Usage

1. **Students**:
   - Submit outpass requests.
   - Mark out and mark in using the facial recognition system.

2. **Admins**:
   - Approve or reject outpass requests.
   - Monitor out students and access historical logs.

---

## Dependencies

The key dependencies include:
- **Flask** for backend functionality.
- **OpenCV** for facial recognition.
- **Firebase Admin** for real-time database operations.
- **Werkzeug** for secure password hashing.

Install them using:
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




