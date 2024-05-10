import flask
import json
import hashlib
import base64
import mysql.connector

f = open("config.json", "r")
data = json.load(f)
key = data["key"]
host = data["host-short"]
port = data["port-short"]
db_host = data["db-host"]
db_user = data["db-user"]
db_passd = data["db-pass"]
db_name = data["db-name"]
f.close()

cnx = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_passd,
    database=db_name
)

cursor = cnx.cursor()

def safe(a):
    return a.replace("'", "\\'").replace('"', '\\"').replace("`", "\\`")

def get_a(uname):
    unamea = safe(uname)
    query = f"SELECT * FROM list WHERE uname = '{unamea}'"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def add(uname, id, url):
    ida = safe(id)
    q = f"SELECT * FROM list WHERE id = '{ida}'"
    cursor.execute(q)
    rk = cursor.fetchall()
    if len(rk)>0:
        return False
    else:
        unamea = safe(uname)
        ida = safe(id)
        urla = safe(url)
        query = f"INSERT INTO list (uname, id, url) VALUES ('{unamea}', '{ida}', '{urla}')"
        cursor.execute(query)
        cnx.commit()
        return True

def delete(uname, id):
    unamea = safe(uname)
    ida = safe(id)
    query = f"DELETE FROM list WHERE uname = '{unamea}' AND id = '{ida}'"
    cursor.execute(query)
    cnx.commit()
    return True

def ch(uname):
    unamea = safe(uname)
    query = f"SELECT * FROM login WHERE uname = '{unamea}'"
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) == 1:
        return True
    else:
        return False

def log(uname, passd):
    passd = safe(passd)
    uname = safe(uname)
    hp = hashlib.sha256(passd.encode()).hexdigest()
    query = f"SELECT * FROM login WHERE uname = '{uname}' AND pass = '{hp}'"
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) == 1:
        return True
    else:
        return False

app = flask.Flask(__name__)


@app.route('/')
def index():
    unamee =  flask.request.cookies.get('uname')
    if unamee == None:
        return flask.render_template('login.html')
    else:
        if ch(ds(unamee, key)): 
            return flask.render_template('index.html')
        else:
            return flask.render_template('login.html')

#login

def es(string, key):
    encoded_string = string.encode('utf-8')
    encoded_key = key.encode('utf-8')
    encrypted_bytes = []
    for i in range(len(encoded_string)):
        encrypted_byte = encoded_string[i] ^ encoded_key[i % len(encoded_key)]
        encrypted_bytes.append(encrypted_byte)
    encrypted_string = base64.b64encode(bytes(encrypted_bytes)).decode('utf-8')
    return encrypted_string

def ds(encrypted_string, key):
    encoded_encrypted_string = encrypted_string.encode('utf-8')
    encoded_key = key.encode('utf-8')
    encrypted_bytes = base64.b64decode(encoded_encrypted_string)
    decrypted_bytes = []
    for i in range(len(encrypted_bytes)):
        decrypted_byte = encrypted_bytes[i] ^ encoded_key[i % len(encoded_key)]
        decrypted_bytes.append(decrypted_byte)
    decrypted_string = bytes(decrypted_bytes).decode('utf-8')
    return decrypted_string

@app.route('/login', methods=['POST'])
def login(methods=['POST']):
    uname = flask.request.form.get('uname')
    passd = flask.request.form.get('pass')
    if log(uname, passd) == True:
        r = flask.Response("ok", status=200)
        r.set_cookie('uname', es(uname, key))
        return r
    else:
        r = flask.Response("no", status=401)
        return r

#login

@app.route('/logout')
def logout():
    r = flask.Response("ok", status=200)
    r.set_cookie('uname', '', expires=0)
    return r

@app.route('/manage', methods=['POST'])
def manage(methods=['POST']):
    unamee = flask.request.cookies.get('uname')
    uname = ds(unamee, key)

    t = flask.request.form.get('type')
    id = flask.request.form.get('id')
    url = flask.request.form.get('url')
    r = flask.Response("ok", 200)

    if t == "add":
        if id == "login" or id == "signup" or id == "manage" or id == "logout":
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

@app.route("/<id>")
def id(id):
    ida = safe(id)
    q = f"SELECT * FROM list WHERE id = '{ida}'"
    cursor.execute(q)
    des = cursor.fetchall()
    if len(des) == 0:
        return flask.render_template("error.html", e="THIS LINK DOESNT EXISTS")
    else:
        return flask.render_template("re.html", des=des[0][2])

@app.route("/signup", methods=["POST", "GET"])
def signup(methods=["POST", "GET"]):
    with open("config.json", "r") as f:
        data = json.load(f)
        if data["signup"] == "true":
            if flask.request.method == "POST":
                uname = flask.request.form.get("uname")
                passd = flask.request.form.get("pass")
                unamea = safe(uname)
                passa = safe(passd)
                hp = hashlib.sha256(passa.encode()).hexdigest()
                query = f"INSERT INTO login (uname, pass) VALUES ('{unamea}', '{hp}')"
                cursor.execute(query)
                cnx.commit()
                r = flask.Response("ok", 200)
                return r
            elif flask.request.method == "GET":
                return flask.render_template("signup.html")
        else:
            return flask.render_template("error.html", "SIGNUP IS DISABLED")

app.run(host=host, port=port)