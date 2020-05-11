import pydub
import os


def reformat(tempo, instruments):
    note_case = ['C', 'Cs', 'D', 'Ds', 'E', 'F',
                 'Fs', 'G', 'Gs', 'A', 'As', 'B']
    note_case = note_case[::-1]
    res = []
    for inst in instruments:
        res.append((inst[0], {}))
        for note in inst[1:]:
            name = (note_case[(note[1] + 11) % 12] +
                    str(8 - (note[1] + 11) // 12))
            if name in res[-1][1]:
                res[-1][1][name].append([note[0] * 7500 // tempo,
                                         note[2] * 7500 // tempo])
            else:
                res[-1][1][name] = [[note[0] * 7500 // tempo,
                                     note[2] * 7500 // tempo]]
        for note in res[-1][1]:
            res[-1][1][note] = sorted(res[-1][1][note], key=lambda x: x[0])
            # Prevent overlay
            for i in range(len(res[-1][1][note]) - 1):
                if sum(res[-1][1][note][i]) >= res[-1][1][note][i + 1][0]:
                    res[-1][1][note][i][1] = res[-1][1][note][i + 1][0] - 1
    return res



# (c) mishgribushenkov, year 2020
#
#       _____________
#      /  mursic.py  \
#      \_____________/
#
class Mursic:
    formats = ('ogg', 'flv', 'mp3', 'aac', 'wav', 'wma')

    def __init__(self, instruments_folder='.', output_folder='.', output_filename='noname',
                 output_formate='wav', output_bitrate='11025'):
        self.inst_folder = instruments_folder
        self.output = (os.path.join(output_folder, output_filename) + '.' + output_formate,
                       output_formate,
                       output_bitrate)

        self.sequence = []
        self.base = {}

    def set_instruments_folder(self, folder):
        self.inst_folder = folder

    def set_output(self, folder='.', filename='noname', formate='wav', bitrate='11025'):
        self.output = (os.path.join(folder, filename) + '.' + formate,
                       formate,
                       bitrate)

    def scan(self):
        log = ''
        instrumentsnames = []
        for i in os.listdir(self.inst_folder):
            if os.path.isdir(os.path.join(self.inst_folder, i)):
                instrumentsnames.append(i)
        totnotenum = 0
        for instrumentname in instrumentsnames:
            log += 'Found instrument ' + instrumentname + '\n'
            notenum = 0
            errornum = 0
            self.base[instrumentname] = {}
            notesnames = os.listdir(os.path.join(self.inst_folder, instrumentname))
            for notename in notesnames:
                self.base[instrumentname][notename[:-4]] = None
                path = os.path.join(self.inst_folder, instrumentname,
                                    notename)
                for i in self.formats:
                    if notename.endswith(i):
                        note = pydub.AudioSegment.from_file(path, format=i)
                        self.base[instrumentname][notename[:-4]] = note
                        log += '\tScanned Note called %s and her Path is: %s\n' % (notename[:-4], path)
                        notenum += 1
                        totnotenum += 1
                        break
                else:
                    log += '\tUnable to scan note at ' + path + '\n'
                    errornum += 1
            log += 'Scanned %i notes. %i errors.\n' % (notenum, errornum)
        log += '_______\n%i instruments with %i notes total added to base!' % (len(instrumentsnames), totnotenum)
        return log

    def play_note(self, instrument, note, starts_at, length):
        if instrument not in self.base.keys():
            return 'Unable to found instrument!'
        if note not in self.base[instrument]:
            return 'Unable to scan note!'
        self.sequence.append((instrument, note, starts_at, length))
        return 'Note successfully played.'

    def set_sequence(self, strange_sequence):
        for i in strange_sequence:
            instrument = i[0]
            if instrument not in self.base.keys():
                return 'Unable to found instrument!'
            for i1 in i[1]:
                note = i1[0]
                if note not in self.base[instrument]:
                    return 'Unable to scan note!'
                for i2 in i1[1:]:
                    self.play_note(instrument, note, i2[0], i2[1])
        return 'Sequence successfully set from your strange sequence.'

    def clear_sequence(self):
        self.sequence = []

    def clear_base(self):
        self.base = {}

    def save(self):
        length = max(*map(lambda x: x[2] + x[3], self.sequence))
        output = pydub.AudioSegment.silent(length + 2000)
        for i in self.sequence:
            note = self.base[i[0]][i[1]]
            note_length = min(i[3] - 1, len(note)) - 1
            output = output.overlay(note[:note_length].fade_out(note_length // 5), i[2] + 1000)  # так вот

        output.export(self.output[0], format=self.output[1], bitrate=self.output[2])


def exampled():
    # initializing
    synthezer = Mursic()
    synthezer.scan()
    synthezer.set_instruments_folder("samples")
    synthezer.set_output(folder="tracks", filename='track', formate='mp3')
    # playing
    synthezer.play_note('pianina', '_30', 0, 5000)
    synthezer.play_note('pianina', '_27', 400, 500)
    synthezer.play_note('pianina', '_28', 800, 500)
    synthezer.play_note('pianina', '_29', 1200, 500)
    synthezer.play_note('pianina', '_28', 1600, 500)
    synthezer.play_note('pianina', '_27', 2000, 500)
    synthezer.play_note('pianina', '_26', 2400, 500)
    synthezer.play_note('pianina', '_26', 2800, 500)
    synthezer.play_note('pianina', '_28', 3200, 500)
    synthezer.play_note('pianina', '_30', 3600, 500)
    synthezer.play_note('pianina', '_29', 4000, 500)
    synthezer.play_note('pianina', '_28', 4400, 500)
    synthezer.play_note('pianina', '_27', 4800, 500)
    synthezer.play_note('pianina', '_28', 5200, 500)
    synthezer.play_note('pianina', '_29', 5600, 500)
    synthezer.play_note('pianina', '_30', 6000, 500)
    synthezer.play_note('pianina', '_28', 6400, 500)
    synthezer.play_note('pianina', '_26', 6800, 500)
    synthezer.play_note('pianina', '_26', 7200, 500)
    synthezer.play_note('pianina', '_29', 7600, 1000)
    synthezer.play_note('pianina', '_31', 8000, 500)
    synthezer.play_note('pianina', '_33', 8400, 500)
    synthezer.play_note('pianina', '_32', 8800, 500)
    synthezer.play_note('pianina', '_31', 9200, 500)
    synthezer.play_note('pianina', '_30', 9600, 500)
    synthezer.play_note('pianina', '_30', 10000, 500)
    synthezer.play_note('pianina', '_28', 10400, 500)
    synthezer.play_note('pianina', '_29', 10800, 500)
    synthezer.play_note('pianina', '_28', 11200, 500)
    synthezer.play_note('pianina', '_27', 11600, 500)
    synthezer.play_note('pianina', '_27', 12000, 500)
    synthezer.play_note('pianina', '_28', 12400, 500)
    synthezer.play_note('pianina', '_29', 12800, 500)
    synthezer.play_note('pianina', '_30', 13200, 500)
    synthezer.play_note('pianina', '_28', 13600, 500)
    synthezer.play_note('pianina', '_26', 14000, 500)
    synthezer.play_note('pianina', '_26', 14400, 2000)

    # saving
    synthezer.save()
    # making it ready to next song
    synthezer.clear_sequence()
