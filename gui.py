import flask
import api.db
import json
import api.check

gui = flask.Blueprint('gui', __name__)

global signup_stat
signup_stat = True

def get():
    with open("config.json", "r") as f:
        data = json.load(f)
        req = data["ext-req"]
        if req:
            return flask.request.headers.get(data["ext-hed"])
        else:
            return flask.request.remote_addr

@gui.route('/')
def index():
    try:
        if api.check.check(flask.request.cookies.get('token'), get()) == 'valid':
            return flask.render_template('index.html')
        else:
            return flask.render_template('login.html')
    except Exception as e:
        print(e)
        return flask.render_template('login.html')

@gui.route('/logout')
def logout():
    r = flask.redirect('/')
    r.set_cookie('token', '', expires=0)
    return r

@gui.route('/signup')
def signup():
    global signup_stat
    if signup_stat:
        return flask.render_template('signup.html')
    else:
        return flask.render_template('error.html', e='SIGNUP IS DISABLED')

@gui.route('/admin', methods=['POST', 'GET'])
def admin():
    global signup_stat
    try:
        if api.check.check(flask.request.cookies.get('token'), get()) == 'valid':
            if api.check.unm == 'admin':
                if flask.request.method == "GET":
                    return flask.render_template('admin.html', stat=signup_stat)
                else:
                    if flask.request.form['act'] == 'd':
                        signup_stat = False
                    elif flask.request.form['act'] == 'e':
                        signup_stat = True
                    return 'hi'
            else:
                return flask.abort(403)
        else:
            return flask.render_template('login.html')
    except Exception as e:
        print(e)
        return flask.render_template('login.html')

@gui.route("/<id>")
def id(id):
    q = "SELECT * FROM list WHERE id = ?"
    api.db.cursor.execute(q, (id,))
    des = api.db.cursor.fetchall()
    if len(des) == 0:
        return flask.abort(404)
    else:
        return flask.render_template("re.html", des=des[0][3])