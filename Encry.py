import os
import urllib.request
import zipfile
import subprocess
import base64
import hashlib
from cryptography.fernet import Fernet
import shutil

def generate_key_from_passphrase(passphrase):
    digest = hashlib.sha256(passphrase.encode()).digest()
    return base64.urlsafe_b64encode(digest[:32])

def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original_data = file.read()

    encrypted_data = fernet.encrypt(original_data)

    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

def download_github_repo(repo_url, dest_folder):
    zip_path = os.path.join(dest_folder, 'repo.zip')
    urllib.request.urlretrieve(repo_url, zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    
    os.remove(zip_path)  # Clean up the zip file

def run_github_project(dest_folder):
    repo_name = os.path.basename(dest_folder)
    entry_point = os.path.join(dest_folder, repo_name, 'run.py')  # Assume 'run.py' is the entry point
    
    if os.path.exists(entry_point):
        subprocess.run(['python', entry_point], check=True)

def self_encrypt(script_path, passphrase):
    key = generate_key_from_passphrase(passphrase)
    encrypt_file(script_path, key)
    print(f"Script encrypted: {script_path}")

def main():
    repo_url = 'https://github.com/yourusername/yourrepository/archive/refs/heads/main.zip'  # Replace with actual URL
    dest_folder = 'downloaded_repo'
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    download_github_repo(repo_url, dest_folder)
    run_github_project(dest_folder)
    
    # Self-encrypt the script
    self_encrypt(__file__, '12345678')  # Ensure you have a backup of the original script

if __name__ == "__main__":
    main()
