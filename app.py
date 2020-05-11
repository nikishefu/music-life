from flask import Flask, render_template, request, send_from_directory, redirect
from forms.track import TrackForm
from audio import *
from models.__all_models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "tHW27uMMNXRuMbwS"
db_session.global_init("db/db.sqlite")

synthezer = Mursic(instruments_folder='samples')
synthezer.scan()

def process_track(data):
    if not(data['title'] and data['tempo'] and data['instruments']):
        return "/error/Invalid_request"
    title = data['title']
    id = count_tracks() + 1
    folder = "tracks"
    filename = f'track{id}'
    formate = 'mp3'
    path = os.path.join(folder, filename + formate)

    synthezer.set_output(folder=folder, filename=filename, formate=formate)

    data = reformat(data['tempo'], data['instruments'])
    for inst in data:
        for note in inst[1]:
            for pos, dur in inst[1][note]:
                synthezer.play_note(inst[0], note, pos, dur)
    try:
        synthezer.save()
    except TypeError:
        return '/error/No_notes_in_available_range'
    else:
        add_track(title, path, 0)
    finally:
        synthezer.clear_sequence()
    return f'/track/{id}'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', page_title='main')

@app.route('/track/<int:track_id>')
def track(track_id):
    if count_tracks() >= track_id:
        return send_from_directory('tracks', f'track{track_id}.mp3')
    else:
        return redirect('/error/Track_not_found')

@app.route('/error/<error_text>')
def error(error_text):
    return render_template('error.html', text=error_text)

@app.route('/track', methods=['GET', 'POST'])
def new_track():
    if request.method == 'GET':
        return render_template('new_track.html', form=TrackForm())
    elif request.method == 'POST':
        if request.json:
            return process_track(request.json)
        else:
            print('ERROR: JSON not found')
            return "/error/JSON_not_found"


if __name__ == '__main__':
    app.run(debug=True)