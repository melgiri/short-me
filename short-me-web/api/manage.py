import flask
from . import api, check, db
import hashlib

@api.route('/signup', methods=['POST'])
def signup():
    uname = flask.request.form.get("uname")
    passd = flask.request.form.get("pass")
    unamea = safe(uname)
    db.cursor.execute(f"SELECT * FROM login WHERE uname = '{unamea}'")
    results = db.cursor.fetchall()
    if len(results) > 0:
        r = flask.Response("no", status=200)
        return r
    else:
        passa = safe(passd)
        hp = hashlib.sha256(passa.encode()).hexdigest()
        query = f"INSERT INTO login (uname, pass) VALUES ('{unamea}', '{hp}')"
        db.cursor.execute(query)
        db.cnx.commit()
        r = flask.Response("ok", 200)
        return r

@api.route('/manage', methods=['POST'])
def manage(methods=['POST']):
    try:
        if check.check(flask.request.cookies.get('set'), flask.request.cookies.get('id')) == 'valid':
            uname = check.unm

            t = flask.request.form.get('type')
            id = flask.request.form.get('id')
            url = flask.request.form.get('url')
            r = flask.Response("ok", 200)

            if t == "add":
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
                for i in range(0, len(get_a(uname))):
                    a += str(get_a(uname)[i]) + "||"
                r.headers.add("res", a)
                return r

            elif t == "del":
                delete(uname, id)
                return r
        else:
            return flask.render_template('login.html')
    except Exception as e:
        print(e)
        return flask.render_template('login.html')


def safe(a):
    return a.replace("'", "\\'").replace('"', '\\"').replace("`", "\\`")

def get_a(uname):
    unamea = safe(uname)
    query = f"SELECT * FROM list WHERE uname = '{unamea}'"
    db.cursor.execute(query)
    results = db.cursor.fetchall()
    return results

def add(uname, id, url):
    ida = safe(id)
    q = f"SELECT * FROM list WHERE id = '{ida}'"
    db.cursor.execute(q)
    rk = db.cursor.fetchall()
    if len(rk)>0:
        return False
    else:
        unamea = safe(uname)
        ida = safe(id)
        urla = safe(url)
        query = f"INSERT INTO list (uname, id, url) VALUES ('{unamea}', '{ida}', '{urla}')"
        db.cursor.execute(query)
        db.cnx.commit()
        return True

def delete(uname, id):
    unamea = safe(uname)
    ida = safe(id)
    query = f"DELETE FROM list WHERE uname = '{unamea}' AND id = '{ida}'"
    db.cursor.execute(query)
    db.cnx.commit()
    return True

def ch(uname):
    unamea = safe(uname)
    query = f"SELECT * FROM login WHERE uname = '{unamea}'"
    db.cursor.execute(query)
    results = db.cursor.fetchall()
    if len(results) == 1:
        return True
    else:
        return False