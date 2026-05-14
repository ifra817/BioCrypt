import os
from cryptography.fernet import Fernet

# Database configuration
DATABASE_PATH = 'data/AttendanceDB'

# Recognition threshold
RECOGNITION_THRESHOLD = 0.6

# Encryption key - generate once and store here
# If not set, generate new one (but for persistence, set it manually or load from .env)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key().decode())

# Save to .env if not exists
if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write(f'ENCRYPTION_KEY={ENCRYPTION_KEY}\n')