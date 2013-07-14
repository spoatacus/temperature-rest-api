from flask import Flask, request, g, json, make_response
import MySQLdb
import ConfigParser

app = Flask(__name__)

config = ConfigParser.SafeConfigParser()
config.read('main.cfg')

DATABASE_HOST = config.get('database', 'host')
DATABASE_NAME = config.get('database', 'name')
DATABASE_USER = config.get('database', 'user')
DATABASE_PASSWORD = config.get('database', 'password')


def connect_db():
    return MySQLdb.connect(host=DATABASE_HOST, user=DATABASE_USER,
            passwd=DATABASE_PASSWORD, db=DATABASE_NAME)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# list of readings
@app.route('/reading', methods=['GET'])
def reading_list():
    cur = get_db().cursor()

    limit = request.values['max'] if 'max' in request.values else 100

    cur.execute("SELECT * FROM reading LIMIT %s", (limit))

    resp = make_response(json.dumps(cur.fetchall()))
    resp.mimetype = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


# latest reading
@app.route('/reading/latest', methods=['GET'])
def reading_latest():
    cur = get_db().cursor()

    limit = request.values['max'] if 'max' in request.values else 100
    print limit

    cur.execute("SELECT * FROM reading ORDER BY timestamp DESC LIMIT %s", (limit))

    resp = make_response(json.dumps(cur.fetchall()))
    resp.mimetype = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


if __name__ == '__main__':
    app.run(debug=True)
