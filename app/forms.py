from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CompareDatesForm(FlaskForm):
    date1 = SelectField('Первая дата', validators=[DataRequired()], choices=[])
    date2 = SelectField('Вторая дата', validators=[DataRequired()], choices=[])
    compare_button = SubmitField('Сравнить расписания')