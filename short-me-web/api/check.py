import json
from secrets import compare_digest
from cryptography.fernet import Fernet
import hashlib

global unm

def check(t_h, i_h):
    with open("config.json", "r") as f:
        data = json.load(f)
        key = data["key"]
        sign = data['sign']
    de = Fernet(key)
    de_a = i_h.split("|.|")
    dt_d = de.decrypt(de_a[0])
    if compare_digest(hashlib.sha256(dt_d).hexdigest(), t_h):
        un_d = de.decrypt(de_a[1])
        global unm
        unm = un_d.decode()
        set_d = dt_d.decode() + un_d.decode() + sign
        set_h = hashlib.sha256(set_d.encode()).hexdigest()
        if compare_digest(set_h, de_a[2]):
            return "valid"
        else:
            return "Invalid sign"
    else:
        return "Something Went Wrong"