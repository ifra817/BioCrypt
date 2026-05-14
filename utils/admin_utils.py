import bcrypt
from .storage_utils import cursor, conn

def create_admin_account(username, password):
    """
    Creates an admin account with hashed password.
    :param username: str
    :param password: str
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute('INSERT INTO Admin(username, password_hash) VALUES(?, ?)', (username, hashed))
    conn.commit()

def verify_admin(username, password):
    """
    Verifies admin credentials.
    :param username: str
    :param password: str
    :return: bool
    """
    cursor.execute('SELECT password_hash FROM Admin WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row:
        return bcrypt.checkpw(password.encode(), row[0])
    return False

def get_attendance_logs(filters=None):
    """
    Retrieves attendance logs with optional filters.
    :param filters: dict, e.g., {'user_id': 1, 'date': '2023-01-01'}
    :return: list of tuples
    """
    query = 'SELECT * FROM Attendance'
    params = []
    if filters:
        conditions = []
        if 'user_id' in filters:
            conditions.append('user_id = ?')
            params.append(filters['user_id'])
        if 'date' in filters:
            conditions.append('timestamp LIKE ?')
            params.append(filters['date'] + '%')
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
    cursor.execute(query, params)
    return cursor.fetchall()

def export_attendance_csv(filename='attendance.csv'):
    """
    Exports attendance logs to CSV.
    :param filename: str
    """
    import csv
    logs = get_attendance_logs()
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'User ID', 'Timestamp'])
        for log in logs:
            writer.writerow(log)