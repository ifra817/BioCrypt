from cryptography.fernet import Fernet
import pickle
from config import ENCRYPTION_KEY

fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_embeddings(embeddings):
    """
    Encrypts the embeddings array.
    :param embeddings: numpy array of face embeddings
    :return: encrypted bytes
    """
    data = pickle.dumps(embeddings)
    return fernet.encrypt(data)

def decrypt_embeddings(encrypted_data):
    """
    Decrypts the encrypted embeddings data.
    :param encrypted_data: encrypted bytes
    :return: numpy array of embeddings
    """
    data = fernet.decrypt(encrypted_data)
    return pickle.loads(data)