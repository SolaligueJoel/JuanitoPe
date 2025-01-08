from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(8, 150)])
    remember = BooleanField('Recordar')
    submit = SubmitField()
