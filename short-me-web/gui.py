import flask
import api.db
import api.check

gui = flask.Blueprint('gui', __name__)

global signup_stat
signup_stat = True

@gui.route('/')
def index():
    try:
        if api.check.check(flask.request.cookies.get('set'), flask.request.cookies.get('id')) == 'valid':
            return flask.render_template('index.html')
        else:
            return flask.render_template('login.html')
    except Exception as e:
        print(e)
        return flask.render_template('login.html')

@gui.route('/logout')
def logout():
    r = flask.Response("ok", status=200)
    r.set_cookie('set', '', expires=0)
    r.set_cookie('id', '', expires=0)
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
        if api.check.check(flask.request.cookies.get('set'), flask.request.cookies.get('id')) == 'valid':
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
                return flask.render_template('error.html', e='You MUST BE ADMIN')
        else:
            return flask.render_template('login.html')
    except Exception as e:
        print(e)
        return flask.render_template('login.html')

@gui.route("/<id>")
def id(id):
    ida = id.replace("'", "\'").replace('"', '\"').replace("`", "\`")
    q = f"SELECT * FROM list WHERE id = '{ida}'"
    api.db.cursor.execute(q)
    des = api.db.cursor.fetchall()
    if len(des) == 0:
        return flask.render_template("error.html", e="THIS LINK DOESNT EXISTS")
    else:
        return flask.render_template("re.html", des=des[0][2])