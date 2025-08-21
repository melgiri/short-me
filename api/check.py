import json
from ast import literal_eval as le
from cryptography.fernet import Fernet
import hashlib

global unm

def check(token, ip):
    with open("config.json", "r") as f:
        data = json.load(f)
        key = data["key"]
        signk = data['sign']
    f = Fernet(key)
    try:
        global unm
        token = f.decrypt(token.encode()).decode()
        token = le(token)
        unm = token[0]
        sign = token[1]
        n_s = signk+ip
        n_s = hashlib.sha256(n_s.encode()).hexdigest()
        if not n_s == sign:
            return False
        return "valid"
    except:
        return False