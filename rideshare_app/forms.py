from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField, URLField, PasswordField, DateField, TimeField, BooleanField
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo, Email, Length


class RideForm(FlaskForm):
    req_date = DateField("Date", validators=[InputRequired()])

    req_time = StringField(
        "Time of departure", validators=[InputRequired()])

    req_dest = StringField(
        "Destination", validators=[InputRequired()])

    rnd_trip = BooleanField(
        "Select if you need the ride to and from the destination")

    dtime_flexibility = StringField(
        "Please mention your flexibility with departure date and time, if any")

    compensation = IntegerField(
        "How much are you willing to pay for the ride?", validators=[InputRequired(),
                                                                     NumberRange(min=10,
                                                                                 message="Please compensate at least $10, thanks.")])
    cmnt = StringField("Additional comments, if any")

    submit = SubmitField("Request Ride")


class RegistrationForm(FlaskForm):
    email = StringField(
        "Enter your Grinnell email address",
        validators=[InputRequired(),
                    Email()]
    )

    name = StringField(
        "Enter your name",
        validators=[InputRequired(),
                    Length(min=4, message="This field should be more than 4 charater long")]
    )

    pwd = PasswordField(
        "Please create a password",
        validators=[InputRequired(),
                    Length(min=4, max=20, message="Passwords need between 4 and 20 characters long")]
    )

    confirm_pwd = PasswordField(
        "Confirm Password",
        validators=[InputRequired(),
                    EqualTo("pwd", message="The passwords do not match")])

    submit = SubmitField(
        "Register"
    )


class LoginForm(FlaskForm):
    email = StringField(
        "Enter your Grinnell email address",
        validators=[InputRequired(),
                    Email()]
    )

    pwd = PasswordField(
        "Enter your passsword",
        validators=[InputRequired()]
    )

    submit = SubmitField(
        "Login"
    )
