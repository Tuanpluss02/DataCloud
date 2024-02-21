import random
import string

def generate_password():
    LENGTH_OF_PASSWORD = 6
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(LENGTH_OF_PASSWORD))
    return password