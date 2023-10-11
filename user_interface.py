import pygame as pg
import json
from cryptography.fernet import Fernet
import base64


point_count = 1010230

class User:
    def __init__(self, username):
        self.user_name = username

    def add_data():
        pass
    def check_score(): 
        pass

############################################################################
# Function to encrypt scores 
def encrypt_data(data, cipher_suite):
    data = str(data)
    return cipher_suite.encrypt(data.encode())

# Function to decrypt scores
def decrypt_data(encrypted_data, cipher_suite):
    return cipher_suite.decrypt(encrypted_data).decode()

############################################################################
# Same for key
def encode_key(key):
    encoded_key = base64.urlsafe_b64encode(key).decode()
    return encoded_key

# Function to decode an encoded key
def decode_key(encoded_key):
    decoded_key = base64.urlsafe_b64decode(encoded_key.encode())
    return decoded_key

############################################################################

# Find key
def search_key():
    # Load existing highscores if the file exists
    try:
        with open(r"Assets\placeholders\placeholder.txt", "r") as file:
            encoded_key = file.read()
            decoded_key = decode_key(encoded_key)
            return decoded_key
    except FileNotFoundError:
        pass

def draw_ui():
    pass

def save_data(encoded_key, encrypted_score):

    # Save the encrypted data to the file
    with open(r"Assets\placeholders\rating.txt", "wb") as file:
        file.write(encrypted_score)
    
    with open(r"Assets\placeholders\placeholder.txt", "w") as file:
        file.write(encoded_key)

def ui(point_count):

    secret_key = search_key()
    
    if not secret_key: 
        # Generate a secret key for encryption. Keep this secret!
        secret_key = Fernet.generate_key()
    
    cipher_suite = Fernet(secret_key)
    
    encrypted_score = encrypt_data(point_count, cipher_suite)
    decrypted_score = decrypt_data(encrypted_score, cipher_suite)
    encoded_key = encode_key(secret_key)
    decoded_key = decode_key(encoded_key)

    #print("encrypt", encrypted_score)
    #print("decrypt", decrypted_score)

    save_data(encoded_key, encrypted_score)




ui(point_count)