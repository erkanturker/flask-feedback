from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,Length

class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(),Length(max=50)])
    first_name = StringField('First Name', validators=[DataRequired(),Length(max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(max=20)])
