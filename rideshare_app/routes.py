import datetime
import functools
from turtle import title
import uuid
from flask import Blueprint, flash, redirect, render_template, current_app, url_for, session
from .models import RideSchema, UserSchema, UserSchema
from .forms import RideForm, RegistrationForm, LoginForm
from dataclasses import asdict, dataclass
from passlib.hash import pbkdf2_sha256

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login_user"))

        return route(*args, **kwargs)

    return route_wrapper


# /API_test
# General case HTML test template
@pages.route("/API_test")
def test_page():
    return render_template(
        template_name_or_list="api_test.html")


# /
# Index (Home page) Route Endpoint
@pages.route("/")
@login_required
def index():
    available_rides = current_app.db.rides_collection.find(
        {"completion_status": {"$ne": "true"}})
    ret_available_rides = [RideSchema(**ride) for ride in available_rides]
    return render_template(
        template_name_or_list="index.html",
        title="Rides @ Grinnell College",
        list_of_available_rides=ret_available_rides)

# /add_ride
# Endpoint to request_ride


@pages.route("/request_ride", methods=["GET", "POST"])
@login_required
def request_ride():
    form = RideForm()

    if form.validate_on_submit():
        input_ride_info = RideSchema(
            _id=uuid.uuid4().hex,
            requester_name=session.get("username"),
            request_date=datetime.datetime.combine(
                form.req_date.data, datetime.time()),
            request_time=form.req_time.data,
            request_destination=form.req_dest.data,
            round_trip=form.rnd_trip.data,
            offered_compensation=form.compensation.data,
            datetime_flexibility=form.dtime_flexibility.data,
            additional_comments=form.cmnt.data
        )

        current_app.db.rides_collection.insert_one(asdict(input_ride_info))

        current_app.db.registered_users.update_one(
            {"_id": session["user_id"]},
            {"$push": {"rides_requested_by_user": input_ride_info._id}}
        )

        return redirect(url_for('.index'))

    return render_template(
        template_name_or_list="new_ride.html",
        title="Rides @ Grinnell - Request a ride",
        form=form)

# /register
# Endpoint to register user


@pages.route("/register", methods=["GET", "POST"])
def register_user():
    if session.get("email"):
        return redirect(url_for('.index'))

    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        user_registration_data = UserSchema(
            _id=uuid.uuid4().hex,
            user_email=registration_form.email.data,
            username=registration_form.name.data,
            user_password=pbkdf2_sha256.hash(registration_form.pwd.data)
        )

        current_app.db.registered_users.insert_one(
            asdict(user_registration_data))
        flash("User registered successfully")
        return redirect(url_for('.login_user'))

    return render_template(
        template_name_or_list="register.html",
        title="Rides @ Grinnell - Register",
        registration_form=registration_form
    )


# /login
# Endpoint to login user
@pages.route("/login", methods=["GET", "POST"])
def login_user():
    if session.get("email"):
        return redirect(url_for(".index"))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_data = current_app.db.registered_users.find_one(
            {"user_email": login_form.email.data})

        if not user_data:
            flash("User with the email address not found", category="danger")
            return redirect(url_for('.login_user'))

        user = UserSchema(**user_data)

        if user and pbkdf2_sha256.verify(login_form.pwd.data, user.user_password):
            session["user_id"] = user._id
            session["username"] = user.username
            session["email"] = user.user_email
            return redirect(url_for('.index'))

        flash("Incorrect login credentials")

    return render_template(
        template_name_or_list="login.html",
        title="Rides @ Grinnell - Login",
        login_form=login_form
    )

# /logout
# Endpoint to logout the user


@pages.route("/logout_user")
@login_required
def logout():
    session.clear()
    return redirect(url_for('.login_user'))

# /my_rideshare_accout
# Endpoint to the user's account


@pages.route("/my_account/<string:_id>")
@login_required
def my_account(_id: str):
    load_user_data = current_app.db.registered_users.find_one(
        {"user_email": session["email"]})
    user_data = UserSchema(**load_user_data)

    load_ride_data = current_app.db.rides_collection.find(
        {"_id": {"$in": user_data.rides_requested_by_user}})
    rides_data = [RideSchema(**ride) for ride in load_ride_data]

    account_name = user_data.username
    return render_template(
        template_name_or_list="my_account.html",
        title=f"Rides @ Grinnell - {account_name}",
        list_of_requested_rides=rides_data)


# /my_account/<_id:uuid.uuid4.hex()>/delete_ride
@pages.route("/my_account/<string:user_id>/delete_ride/<string:ride_id>")
@login_required
def delete_ride(user_id:str,ride_id:str):
    current_app.db.rides_collection.delete_one({
        "_id":ride_id
    })

    return redirect(url_for('.my_account',_id=user_id))
    