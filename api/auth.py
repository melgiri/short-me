import flask
from . import api
from . import db
import json
import hashlib
from secrets import compare_digest
from cryptography.fernet import Fernet

def get():
    with open("config.json", "r") as f:
        data = json.load(f)
        req = data["ext-req"]
        if req:
            return flask.request.headers.get(data["ext-hed"])
        else:
            return flask.request.remote_addr

def set(un, ip):
    with open("config.json", "r") as f:
        data = json.load(f)
        key = data["key"]
        sign = data['sign']
    f = Fernet(key)
    sign_key_f = sign + ip
    sign = hashlib.sha256(sign_key_f.encode()).hexdigest()
    t_a = str([un, sign])
    token = f.encrypt(t_a.encode()).decode()
    return token


@api.route('/auth', methods=['POST'])
def auth():
    uname = flask.request.form['uname']
    passd = flask.request.form['pass']

    db.cursor.execute("SELECT pass FROM login WHERE uname = ?", (uname,))
    p = db.cursor.fetchall()
    if len(p) == 0:
        return "Invalid username"
    else:
        if compare_digest(hashlib.sha256(passd.encode()).hexdigest(), p[0][0]):
            r = flask.make_response("Logged in")
            r.set_cookie("token", set(uname, get()), max_age=1209600)
            return r
        else:
            return "Invalid password"