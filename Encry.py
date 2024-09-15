import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key_from_passphrase(passphrase):
    """
    Generates a Fernet key from a passphrase.

    Args:
        passphrase (str): The passphrase to convert.

    Returns:
        bytes: A valid Fernet key.
    """
    digest = hashlib.sha256(passphrase.encode()).digest()
    return base64.urlsafe_b64encode(digest[:32])

def encrypt_file(file_path, key):
    """
    Encrypts the content of a file and writes it back as encrypted.

    Args:
        file_path (str): Path to the file to encrypt.
        key (bytes): Encryption key.
    """
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original_data = file.read()

    encrypted_data = fernet.encrypt(original_data)

    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as file:
        file.write(encrypted_data)
    
    print(f"File encrypted and saved as {encrypted_file_path}")

def main():
    file_to_encrypt = 'Wor.py'  # Specify your actual file name here
    passphrase = '12345678'  # Use a secure passphrase

    # Generate an encryption key
    encryption_key = generate_key_from_passphrase(passphrase)

    # Encrypt the specified file
    encrypt_file(file_to_encrypt, encryption_key)

if __name__ == "__main__":
    main()
