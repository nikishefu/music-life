from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class TrackForm(FlaskForm):
    title = StringField('Название трека', validators=[DataRequired()])
    tempo = IntegerField('Темп', validators=[DataRequired()])
    instrument = SelectField('Инструмент', choices=[('guitar', 'Гитара')], validators=[DataRequired()])
    submit = SubmitField('Сохранить')