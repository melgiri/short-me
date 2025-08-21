from cryptography.fernet import Fernet
import json

with open('config.json', 'r') as f:
    p = json.load(f)
    p['key'] = Fernet.generate_key().decode()
    with open('config.json', 'w') as f:
        json.dump(p, f)
