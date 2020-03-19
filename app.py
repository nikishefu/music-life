from flask import Flask, render_template


app = Flask(__name__)
@app.route('/')
@app.route('/index')

def main_page():

	render_template('index.html', page_title='main')

if __name__ == '__main__':

	app.run(port=8080, host='127.0.0.1')