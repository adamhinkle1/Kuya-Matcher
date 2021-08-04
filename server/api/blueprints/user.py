from flask import Blueprint, current_app, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from server.api.extensions import limiter, db
#from server.api.models import Question_Set, Answer, User
from server.api.models import User
from server.api.constants import LITTLE_QUESTION_SET_ID, BIG_QUESTION_SET_ID
from server.api.gmail_sender import send_little_confirm_emails, send_big_confirm_emails
from server.api.utils import google_client, get_google_provider_cfg, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
import requests

user_bp = Blueprint('user', __name__)


@user_bp.route("/user")
@user_bp.route("/user/")
@limiter.limit("2 per second")
def index():

    return "user index page"


@user_bp.route("/user/is_admin")
@limiter.limit("2 per second")
def logged_in():
    if  current_user.is_authenticated and current_user.is_admin:
        #logged in
        return "you are admin"
    else:
        # are not logged in
        return ""


@user_bp.route("/user/info")
@login_required
@limiter.limit("2 per second")
def user_info():
    db_user = User.query.filter(User.id == current_user.id).first()
    if not db_user:
        return "user not exist", 403

    return db_user.get_json()
