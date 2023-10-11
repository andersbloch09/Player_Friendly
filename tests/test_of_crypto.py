import json
from cryptography.fernet import Fernet
import base64

# Generate a secret key for encryption. Keep this secret!
secret_key = Fernet.generate_key()
cipher_suite = Fernet(secret_key)

# Function to encrypt data
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

# Function to decrypt data
def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode()

def encode_key(key):
    encoded_key = base64.b64encode(key)
    return encoded_key

# Save highscore
def save_highscore(username, score):
    highscores = {}

    # Load existing highscores if the file exists
    try:
        with open("highscores.txt", "rb") as file:
            encrypted_data = file.read()
            highscores = json.loads(decrypt_data(encrypted_data))
    except FileNotFoundError:
        pass

    # Update or add the user's highscore
    highscores[username] = score

    # Serialize and encrypt the updated data
    encrypted_data = encrypt_data(json.dumps(highscores))
    
    # Save the encrypted data to the file
    with open("highscores.txt", "wb") as file:
        file.write(encrypted_data)
    
    encoded_key = encode_key(secret_key)
    print(encoded_key)

    with open("highscores.txt", "wb") as file:
        file.write(encrypted_data)

# Load and display highscores
def load_highscores():
    try:
        with open("highscores.txt", "rb") as file:
            encrypted_data = file.read()
            highscores = json.loads(decrypt_data(encrypted_data))
            for username, score in highscores.items():
                print(f"{username}: {score}")
    except FileNotFoundError:
        print("No highscores yet.")

# Example usage
save_highscore("player1", 1000)
save_highscore("player2", 800)
load_highscores()
