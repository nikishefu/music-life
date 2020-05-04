from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = "tHW27uMMNXRuMbwS"

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

@app.route('/track', methods=['GET', 'POST'])
def new_track():
	if request.method == 'GET':
		return render_template('new_track.html')
	elif request.method == 'POST':
		if request.json:
			print(request.json['tempo'])
			return 'OK'
		else:
			print('ERROR')
			return 'Error'


if __name__ == '__main__':
	app.run()