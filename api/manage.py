import flask
from . import api, check, db
import hashlib
import json

def get():
    with open("config.json", "r") as f:
        data = json.load(f)
        req = data["ext-req"]
        if req:
            return flask.request.headers.get(data["ext-hed"])
        else:
            return flask.request.remote_addr


@api.route('/signup', methods=['POST'])
def signup():
    uname = flask.request.form.get("uname")
    passd = flask.request.form.get("pass")
    db.cursor.execute("SELECT * FROM login WHERE uname = ?", (uname,))
    results = db.cursor.fetchall()
    if len(results) > 0:
        r = flask.Response("no", status=200)
        return r
    else:
        hp = hashlib.sha256(passd.encode()).hexdigest()
        query = "INSERT INTO login (uname, pass) VALUES (?, ?)"
        db.cursor.execute(query, (uname, hp))
        db.cnx.commit()
        r = flask.Response("ok", 200)
        return r

@api.route('/manage', methods=['POST'])
def manage(methods=['POST']):
    try:
        if check.check(flask.request.cookies.get('token'), get()) == 'valid':
            uname = check.unm

            t = flask.request.form.get('type')
            id = flask.request.form.get('id')
            r = flask.Response("ok", 200)

            if t == "add":
                url = flask.request.form.get('url')
                if id == "api/auth" or id == "signup" or id == "api/manage" or id == "logout" or id == "admin":
                    r = flask.Response("noa", status=401)
                    return r
                else:
                    if add(uname, id, url) == True:
                        return r
                    else:
                        r = flask.Response("no", status=401)
                        return r

            elif t == "get":
                a = ""
                re = get_a(uname)
                for i in re:
                    a += str(i) + "||"
                r.headers.add("res", a)
                return r

            elif t == "del":
                delete(uname, id)
                return r
            elif t == "edit":
                url = flask.request.form.get('url')
                id_n = flask.request.form.get('id_n')
                if not edit(uname, id, id_n, url):
                    r = flask.Response("no", status=401)
                return r
        else:
            return flask.render_template('login.html')
    except Exception as e:
        print(e)
        return flask.render_template('login.html')


def get_a(uname):
    query = "SELECT * FROM list WHERE uname = ?"
    db.cursor.execute(query, (uname,))
    results = db.cursor.fetchall()
    return results

def add(uname, id, url):
    q = "SELECT * FROM list WHERE id = ?"
    db.cursor.execute(q, (id,))
    rk = db.cursor.fetchall()
    if len(rk)>0:
        return False
    else:
        query = "INSERT INTO list (sl, uname, id, url) VALUES (?, ?, ?, ?)"
        db.cursor.execute(query, (uname+"_"+id, uname, id, url))
        db.cnx.commit()
        return True

def edit(uname, id_o, id_n, url):
    q = "SELECT * FROM list WHERE id = ? AND uname = ?"
    db.cursor.execute(q, (id_n, uname))
    rk = db.cursor.fetchall()
    if len(rk) != 0:
        if id_o != rk[0][0]:
            print(id_o, rk[0][0])
            return False
    query = "UPDATE list SET id = ?, url = ? WHERE uname = ? AND sl = ?"
    db.cursor.execute(query, (id_n, url, uname, id_o))
    db.cnx.commit()
    return True

def delete(uname, id):
    query = "DELETE FROM list WHERE uname = ? AND id = ?"
    db.cursor.execute(query, (uname, id))
    db.cnx.commit()
    return True