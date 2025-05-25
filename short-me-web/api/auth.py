import flask
from . import api
from . import db
import json
import hashlib
from secrets import compare_digest
import datetime
from cryptography.fernet import Fernet

def set(un):
    global time, token
    dt = str(datetime.datetime.now())
    with open("config.json", "r") as f:
        data = json.load(f)
        key = data["key"]
        sign = data['sign']
    f = Fernet(key)
    t = f.encrypt(dt.encode())
    time = hashlib.sha256(dt.encode()).hexdigest()
    u = f.encrypt(un.encode())
    set = dt+un+sign
    h = hashlib.sha256(set.encode()).hexdigest()
    token = t.decode()+"|.|"+u.decode()+"|.|"+h


@api.route('/auth', methods=['POST'])
def auth():
    uname = flask.request.form['uname'].replace("'", "\'").replace('"', '\"').replace("`", "\`")
    passd = flask.request.form['pass'].replace("'", "\'").replace('"', '\"').replace("`", "\`")

    db.cursor.execute(f"SELECT pass FROM login WHERE uname = '{uname}'")
    p = db.cursor.fetchall()
    if len(p) == 0:
        return "Invalid username"
    else:
        if compare_digest(hashlib.sha256(passd.encode()).hexdigest(), p[0][0]):
            set(uname)
            global time, token
            r = flask.make_response("Logged in")
            r.set_cookie("set", time)
            r.set_cookie('id', token)
            return r
        else:
            return "Invalid password"