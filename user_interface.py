import pygame as pg
from cryptography.fernet import Fernet
import base64
import time 
       
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
        with open(r"Assets/placeholders/placeholder.txt", "r") as file:
            encoded_key = file.read()
            decoded_key = decode_key(encoded_key)
            return decoded_key
    except FileNotFoundError:
        pass


def save_data(encoded_key, encrypted_score):

    # Save the encrypted data to the file
    with open(r"Assets/placeholders/rating.txt", "wb") as file:
        file.write(encrypted_score)
    
    with open(r"Assets/placeholders/placeholder.txt", "w") as file:
        file.write(encoded_key)

def read_data():
    # Opens both files as read to get the data after it decodes the data
    with open(r"Assets/placeholders/rating.txt", "rb") as file:
        encrypted_data = file.read()
    
    with open(r"Assets/placeholders/placeholder.txt", "r") as file:
        secret_key = file.read()

    decoded_key = decode_key(secret_key)
    cipher_suite = Fernet(decoded_key)

    decrypted_data = decrypt_data(encrypted_data, cipher_suite)

    print(decrypted_data)

# Class for ui buttons
class buttons(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, initial_width, initial_height, image, window, scale_factor, image_clicked = 0):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.none_clicked = image
        self.image_clicked = image_clicked
        self.start_time = time.time()
        self.start_b = False
        self.image = pg.transform.smoothscale(self.image, (initial_width*scale_factor, initial_height*scale_factor))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x*scale_factor, pos_y*scale_factor]
        self.window = window

    def draw_click(self, mouse_pos=None):
        if self.image_clicked != 0:
            self.check_time = time.time()
            if mouse_pos:
                self.image = self.image_clicked
                if self.start_b == True:
                    time.sleep(0.25)
                self.start_time = time.time()
                if self.start_time - self.check_time > 0.25: 
                    self.image = self.none_clicked
                    if self.start_b == True: 
                        return False
                    else: 
                        return True

    def button_filter(self, button_index):
        self.start_b = False
        print(button_index)
        if button_index == 0: 
            self.start_b = True
       

    def draw(self): 
        self.window.blit(self.image, (self.rect.topleft[0], self.rect.topleft[1]))

# This function will create all the objects for the ui 
def create_buttons(ui_button_group, WIN, scale_factor): 
    ##########################################################################################################
    # UI sprites
    add_button = pg.image.load("Assets/ui_assets/add_button.png").convert_alpha()
    add_button_clicked = pg.image.load("Assets/ui_assets/add_button_clicked.png").convert_alpha()
    arrow_button = pg.image.load("Assets/ui_assets/arrow.png").convert_alpha()
    arrow_button_clicked = pg.image.load("Assets/ui_assets/arrow_clicked.png").convert_alpha()
    remove_button = pg.image.load("Assets/ui_assets/remove.png").convert_alpha()
    remove_button_clicked = pg.image.load("Assets/ui_assets/remove_clicked.png").convert_alpha()
    start_button = pg.image.load("Assets/ui_assets/start_button.png").convert_alpha()
    start_button_clicked = pg.image.load("Assets/ui_assets/start_button_clicked.png").convert_alpha()
    table_sign = pg.image.load("Assets/ui_assets/table_sign.png").convert_alpha()
    add_button_ob = buttons(500, 800-214, 310, 214, add_button, WIN, scale_factor, add_button_clicked)
    arrow_button_ob = buttons(1025, 137, 120, 105, arrow_button, WIN, scale_factor, arrow_button_clicked)
    remove_button_ob = buttons(1221, 10, 300, 142, remove_button, WIN, scale_factor, remove_button_clicked)
    start_button_ob = buttons(100, 800-228, 325, 231, start_button, WIN, scale_factor, start_button_clicked)
    table_sign_ob = buttons(1100, 800-688, 548, 688, table_sign, WIN, scale_factor)
    ui_button_group.add(
        start_button_ob,
        add_button_ob,
        arrow_button_ob,
        remove_button_ob,
        table_sign_ob
    )
    
    return ui_button_group

def ui():
    secret_key = search_key()
    
    if not secret_key: 
        # Generate a secret key for encryption. Keep this secret!
        secret_key = Fernet.generate_key()
    
    cipher_suite = Fernet(secret_key)
    
    # encrypted_score = encrypt_data(point_count, cipher_suite)
    
    encoded_key = encode_key(secret_key)
    

    #print("encrypt", encrypted_score)
    #print("decrypt", decrypted_score)

    # save_data(encoded_key, encrypted_score)
    read_data()
