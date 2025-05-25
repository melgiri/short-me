import flask
from api import api, db
from gui import gui

app = flask.Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(gui, url_prefix='/')

if __name__ == '__main__':
    app.run(host=db.host, port=db.port)
