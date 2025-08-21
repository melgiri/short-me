import flask
from api import api, db
from gui import gui
import waitress

app = flask.Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(gui, url_prefix='/')

@app.errorhandler(403)
def forbidden(e):
    return flask.render_template('error.html', e="Forbidden access"), 403

@app.errorhandler(404)
def not_found(e):
    return flask.render_template('error.html', e="Not found"), 404

if __name__ == '__main__':
    waitress.serve(app, host=db.host, port=db.port, threads=4)