from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class ArrowForm(FlaskForm):
    direction = RadioField('Select the direction',
                           choices=[(0, 'Left'), (1, 'Up'), (2, 'Down'), (3, 'Right')],
                           validators=[DataRequired()],
                           default=3)
    submit = SubmitField('Move')


class CustomGameForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()], default='John Doe')
    size = IntegerField('Enter size of the level(10-20)', validators=[DataRequired(), NumberRange(min=4, max=20)],
                        default=10)
    rate = IntegerField('Enter snow rate(60-80)', validators=[DataRequired(), NumberRange(min=1, max=100)],
                        default=70)
    terrain = SelectField('Choose terrain',
                          choices=['lava', 'sand', 'rock'],
                          validators=[DataRequired()],
                          default=0)
    submit = SubmitField('Start Custom Game')


class GameCreationForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()], default='John Doe')
    level = SelectField('Choose level size',
                        coerce=int,
                        choices=[(3, '3x3'), (5, '5x5'), (7, '7x7')],
                        validators=[DataRequired()],
                        default=0)
    submit = SubmitField('Start Game')
