from flask import Blueprint, current_app, request, redirect, url_for, render_template
from flask_login import login_required
from server.api.extensions import limiter, db
#from server.api.models import Question_Set, Answer
from server.api.constants import LITTLE_QUESTION_SET_ID, BIG_QUESTION_SET_ID
from server.api.gmail_sender import send_little_confirm_emails, send_big_confirm_emails

board_member_bp = Blueprint('board_member', __name__)

@board_member_bp.route("/board_member")
@board_member_bp.route("/board_member/")
@limiter.limit("2 per second")
def index():

    return "board member index page"
