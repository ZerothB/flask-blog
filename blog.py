#blog.py controller

#imports

from flask import *
import sqlite3

#configuration

USERNAME='admin'
PASSWORD='admin'
SECRET_KEY='rM\xb1\xdc\x12o\xd6i\xff+9$T\x8e\xec\x00\x13\x82.*\x16TG\xbd'
DATABASE='blog.db'
DEBUG=True

app = Flask(__name__)


app.config.from_object(__name__)


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


@app.route('/', methods=['GET', 'POST'])
def login():
	error=None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))


	return render_template('login.html', error=error)

@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
	app.run()