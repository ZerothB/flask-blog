#blog.py controller

#imports

from flask import *
from functools import wraps
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


def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if session['logged_in']:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap




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
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('select * from posts')
	posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
	g.db.close()
	return render_template('main.html', posts=posts)


@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash("All fields are required. Please try again.")
		return redirect(url_for('main'))
	else:
		print title, post
		print request.form['title']
		g.db=connect_db()
		g.db.execute('insert into posts (title, post) values (?, ?)', [request.form['title'], request.form['post']])
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted!')
		return redirect(url_for('main'))


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run()