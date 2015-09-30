#blog.py controller

#imports

from flask import *
import sqlite3

#configuration

DATABASE='blog.db'
DEBUG=True

app = Flask(__name__)


app.config.from_object(__name__)


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


@app.route('/')
def login():

	return render_template('login.html')

@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
	app.run()