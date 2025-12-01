import sqlite3

conn = sqlite3.connect('data/AttendanceDB')
cursor = conn.cursor()

cursor.executescript('''
    DROP TABLE IF EXISTS Students;
    DROP TABLE IF EXISTS Encodings;
    CREATE TABLE Students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        registrationNo TEXT UNIQUE NOT NULL
    );
    CREATE TABLE Encodings (
        id INTEGER AUTOINCREMENT
        face_id INT references ID,
        embeddings BLOB UNIQUE
    );
''')

def createStudent(name, registrationNo):
    cursor.execute('''
        INSERT INTO Students(name, registrationNo) VALUES(?, ?);
    ''', (name, registrationNo))
    print("Student added in the table successfully 👌")

def save_embeddings(id, embeddings):
    cursor.execute('''
        INSERT INTO Encodings()
    ''')