# 🟦 Face Recognition Attendance System

A lightweight, interactive console-based attendance system powered by facial recognition using Python, OpenCV, and SQLite.

## 📌 Overview

This project implements a local facial-recognition–based attendance system. Users can register their face, store their embeddings in an SQLite database, and later mark attendance by simply showing their face to the webcam.

The system is designed to be:

- **Lightweight**
- **CPU-friendly** (no GPU required)
- **Modular and clean**
- **Easy to run** inside VS Code or any terminal

It uses HOG-based face detection and captures one high-quality snapshot to extract reliable embeddings.

## 🧠 Key Features

### ✔ Face Registration
- Live face detection through webcam
- Waits for stable face before capturing
- Extracts 128-D face embeddings
- Stores into SQLite database:
  - Username
  - Email
  - Auto-generated User ID
  - Face embeddings

### ✔ Face Recognition / Attendance Marking
- Real-time webcam feed
- Embedding extraction
- Matching with registered users
- On success → logs attendance with timestamp
- Attendance history stored locally

### ✔ Fully Local
- No internet required
- Uses SQLite database
- Fast, secure, and offline

### ✔ Lightweight Optimization
- HOG face detection (CPU-safe)
- Processes only one stable frame
- Suitable for laptops without GPU/CUDA


## 🧱 Project Structure
```bash
FaceRecognition/
│
├── face_register.py # Register new users
├── face_login.py # Mark attendance using face recognition
├── main.py # Runs app
├── config.py # For database configuration
│
├── utils/
│ ├── capture_utils.py # Webcam, detection, embeddings
│ ├── storage_utils.py # SQLite operations
│ └── init.py
│
├── database/
│ └── attendance.db # SQLite DB (auto-created)
│
├── README.md # Documentation
└── env/ # Virtual environment
```


## 🧩 Modules Breakdown

### 🔹 1. `capture_utils.py`
Handles all camera-related operations:
- Opening webcam
- Capturing frames
- Detecting faces
- Drawing bounding boxes
- Taking snapshots
- Generating embeddings

### 🔹 2. `storage_utils.py`
Handles all database operations:
- Creating tables
- Saving user info
- Storing embeddings
- Fetching embeddings for matching
- Logging attendance records

### 🔹 3. `face_register.py`
Console-based registration workflow:
- Ask for user's name & email
- Start webcam
- Detect stable face
- Extract embeddings
- Save to database
- Print success message

### 🔹 4. `face_login.py` (attendance)
Runs the recognition workflow:
- Detect and extract face
- Compare with DB
- If matched → mark attendance
- Show user-friendly console output


## 🛠 Tech Stack

**Core Logic**
- Python 3.x
- SQLite3

**Computer Vision & Machine Learning**
- OpenCV
- `face_recognition` (dlib)
- NumPy

**Development Environment**
- Visual Studio Code
- Python Virtual Environment (venv)


## 🚀 How It Works (Workflow)

### Step 1 — Register User
Run:
```bash
python face_register.py
```
- Enter name & email

- Webcam opens

- System waits for stable face

- Captures frame → extracts embeddings

- Saves to SQLite

Step 2 — Mark Attendance
Run:

```bash
python face_login.py
```
- Look at the camera

- System extracts embeddings

- Compares with database

- If match → logs attendance:

- Welcome <name> — Attendance Marked.


📦 Installation & Setup

1. Clone the Repository
```bash
git clone <your_repo_link>
cd FaceRecognition
```
2. Create Virtual Environment
```bash
python -m venv env
```
3. Activate it
Windows:

```bash
env\Scripts\activate
```
macOS/Linux:

```bash
source env/bin/activate
```

4. Install Dependencies
```bash
pip install -r requirements.txt
```

5. Run
For registration:

```bash
python face_register.py
```
For attendance:

```bash
python face_login.py
```

⚠️ Important Notes
- HOG-based detector is CPU-friendly but slower

- Only one stable frame is used to extract embeddings

- Ensures laptop does not hang or overheat

- Ideal for:

  - University projects

  - Small offices/labs

  - Local attendance systems

📎 Future Enhancements (Optional)
- GUI using Tkinter or PyQt

- GPU-accelerated embedding extractor

- Flask API for web-based attendance

- Multi-face support

- Admin dashboard for attendance analytics


