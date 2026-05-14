import sqlite3
from .security_utils import encrypt_embeddings, decrypt_embeddings
from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        registrationNo TEXT UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Encodings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        face_id INTEGER REFERENCES Students(id),
        embeddings BLOB
    );
    CREATE TABLE IF NOT EXISTS Attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES Students(id),
        timestamp TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
''')

def createStudent(name, registrationNo):
    cursor.execute('''
        INSERT INTO Students(name, registrationNo) VALUES(?, ?);
    ''', (name, registrationNo))
    conn.commit()
    print("Student added in the table successfully 👌")

def save_embeddings(id, embeddings):
    encrypted = encrypt_embeddings(embeddings)
    cursor.execute('''
        INSERT INTO Encodings(face_id, embeddings) VALUES(?, ?);
    ''', (id, encrypted))
    conn.commit()

def get_embeddings_for_user(user_id):
    cursor.execute('SELECT embeddings FROM Encodings WHERE face_id = ?', (user_id,))
    row = cursor.fetchone()
    if row:
        return decrypt_embeddings(row[0])
    return None

def mark_attendance(user_id, timestamp):
    cursor.execute('INSERT INTO Attendance(user_id, timestamp) VALUES(?, ?)', (user_id, timestamp))
    conn.commit()

def get_all_users():
    cursor.execute('SELECT id, name, registrationNo FROM Students')
    return cursor.fetchall()