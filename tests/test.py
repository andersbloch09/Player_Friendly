import base64

def encode_key(key):
    encoded_key = base64.b64encode(key)
    return encoded_key

# Function to decode an encoded key
def decode_key(encoded_key):
    decoded_key = base64.b64decode(encoded_key.encode()).decode()
    return decoded_key

key = 3429024130


