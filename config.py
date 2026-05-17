import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Force load variables from the .env file into os.environ
load_dotenv()

# Database configuration
DATABASE_PATH = 'data/AttendanceDB'

# Recognition threshold
RECOGNITION_THRESHOLD = 0.6

# Now os.getenv will successfully see the saved key from your .env file!
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

# Fallback block if .env didn't exist yet
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    with open('.env', 'w') as f:
        f.write(f'ENCRYPTION_KEY={ENCRYPTION_KEY}\n')