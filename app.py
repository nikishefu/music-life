from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', page_title='main')

@app.route('/user/<int:user_id>')
def user(user_id):
	# TODO get user data by user_id
	return render_template('user.html', user=None  # User data
	)

@app.route('/track/<int:track_id>')
def track(track_id):
	# TODO get track data by track_id
	return render_template('track.html', track_id=None  # Track data
	)

if __name__ == '__main__':
	app.run()