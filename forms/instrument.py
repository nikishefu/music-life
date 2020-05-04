from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class instrument_form(FlaskForm):
    tempo = IntegerField('Темп', validators=[DataRequired()])
    instrument = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('Сохранить')