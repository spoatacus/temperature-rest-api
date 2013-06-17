from flask import Flask, g, json, make_response
import MySQLdb

app = Flask(__name__)

DATABASE_HOST = '10.10.2.10'
DATABASE_NAME = 'arduino_weather'
DATABASE_USER = 'weather'
DATABASE_PASSWORD = 'weather'


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
@app.route("/reading", methods=['GET'])
def reading_list():
	cur = get_db().cursor()
	cur.execute("SELECT * FROM reading")

	resp = make_response(json.dumps(cur.fetchall()))
	resp.mimetype = 'application/json'
	resp.headers['Access-Control-Allow-Origin'] = '*'

	return resp


if __name__ == '__main__':
	app.run(debug=True)
