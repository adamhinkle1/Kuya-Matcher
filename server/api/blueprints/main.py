from flask import Blueprint, current_app, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from server.api.extensions import limiter, db
#from server.api.models import Question_Set, Answer
from server.api.models import Big_Question_Set, Little_Question_Set, Big_Answer, Little_Answer
from server.api.constants import LITTLE_QUESTION_SET_ID, BIG_QUESTION_SET_ID
from server.api.gmail_sender import send_little_confirm_emails, send_big_confirm_emails
from server.api.forms.admin import Send_Little_Email_Form, Send_Big_Email_Form
import os
from server.api.utils import submission_json_to_database_json
from server.api.constants import BIG_QUESTION_SET_ID, LITTLE_QUESTION_SET_ID

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@limiter.limit("2 per second")
def index():
    #FIXME: for now
    #return "this is index page for the 445APP"

    #FIXME: this line will be used in actual program
    return current_app.send_static_file('index.html')



@main_bp.route("/test")
@login_required
@limiter.limit("2 per second")
def test():
    return "logged in..."


#user 'get' to get the question set, 'post' to update it
@main_bp.route("/main/question_set/little")
@limiter.limit("2 per second")
def little_question_set():
    #one_question_set = Little_Question_Set.query.filter(Question_Set.id == LITTLE_QUESTION_SET_ID).first()
    one_question_set = Little_Question_Set.query.first()

    if request.method == 'GET':
        #get question-set json
        if one_question_set:
            #return {"questions" : one_question_set.get_json()}
            return one_question_set.get_json()
            #return render_template("/main/questions_set_little.html", questions_set=one_question_set.get_json())
            #return one_question_set.get_json()
        # {"questions":[{"....":[possible answers]}, {"....":[possible_answers]}, "{....: [possible_answers]}"]}
        return {}


#user 'get' to get the question set, 'post' to update it
@main_bp.route("/main/question_set/big")
@limiter.limit("2 per second")
def big_question_set():
    #one_question_set = Question_Set.query.filter(Question_Set.id == BIG_QUESTION_SET_ID).first()
    one_question_set = Big_Question_Set.query.first()

    if request.method == 'GET':
        #get question_set json
        if one_question_set:
            #return {"questions" : one_question_set.get_json()}
            return one_question_set.get_json()
        # {"questions":[{"....":[possible answers]}, {"....":[possible_answers]}, "{....: [possible_answers]}"]}
        return {}



#answer should be in form of {1:"...", 2:"...", 3:"..."} (preferred)
#or {'answers': [..., ..., ...,]}
@main_bp.route("/main/question_set/big/answer_new", methods=['POST'])
@limiter.limit("2 per second")
def big_answer_new():
    one_submission_json = request.get_json()

    #if submission json is empty
    if not one_submission_json:
        print("---empty big detected...")
        return redirect(url_for('main.index'))

    #covert to what the database need
    processed_json = submission_json_to_database_json(BIG_QUESTION_SET_ID, one_submission_json)


    #save the processed version to database
    db_Answer_new = Big_Answer()
    db_Answer_new.answers_json = processed_json
    db_Answer_new.question_set_id = BIG_QUESTION_SET_ID
    db_Answer_new.name = processed_json['name']
    db_Answer_new.email = processed_json['email']
    db_Answer_new.age = processed_json['age']
    db_Answer_new.major_dept = processed_json['major_dept']
    db_Answer_new.major = processed_json['major']

    db.session.add(db_Answer_new)
    db.session.commit()
    return redirect(url_for('main.index'))

#answer should be in form of {1:"...", 2:"...", 3:"..."} (preferred)
#or {'answers': [..., ..., ...,]}
@main_bp.route("/main/question_set/little/answer_new", methods=['POST'])
@limiter.limit("2 per second")
def little_answer_new():
    one_submission_json = request.get_json()

    if not one_submission_json:
        print("---empty little submission detected...")
        return redirect(url_for('main.index'))

    #covert to what the database need
    processed_json = submission_json_to_database_json(LITTLE_QUESTION_SET_ID, one_submission_json)

    db_Answer_new = Little_Answer()
    db_Answer_new.answers_json = processed_json
    db_Answer_new.question_set_id = LITTLE_QUESTION_SET_ID
    db_Answer_new.name = processed_json['name']
    db_Answer_new.email = processed_json['email']
    db_Answer_new.age = processed_json['age']
    db_Answer_new.major_dept = processed_json['major_dept']
    db_Answer_new.major = processed_json['major']

    db.session.add(db_Answer_new)
    db.session.commit()
    return redirect(url_for('main.index'))



#FIXME: test
@main_bp.route("/main/test_email/little/<one_email>")
@login_required
@limiter.limit("1 per second")
def send_confirmation_email_little(one_email):
    email_list = [one_email]
    send_little_confirm_emails(email_list)


    return "sent to little..."

#FIXME: test
@main_bp.route("/main/test_email/big/<one_email>")
@login_required
@limiter.limit("1 per second")
def send_confirmation_email_big(one_email):
    email_list = [one_email]
    send_big_confirm_emails(email_list)

    return "sent to big..."

