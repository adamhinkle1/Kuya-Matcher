from flask import Blueprint, render_template, flash, redirect, url_for, jsonify, request, Response, send_file
from flask_login import current_user, login_required
from server.api.extensions import limiter, db
from server.api.decorators import is_admin
from server.api.forms.admin import Send_Big_Email_Form, Send_Little_Email_Form, Notify_Event_Form, Upload_Result_Form, Upload_Question_Set_Form, Confirmation_Email_Form
from server.api.gmail_sender import send_little_confirm_emails, send_big_confirm_emails
#from server.api.models import Question_Set, Answer, Matching_Point, Big_Answer
from server.api.models import Big_Question_Set, Matching_Point, Big_Answer, Little_Question_Set, Little_Answer, Confirmation_Email_Message
#from server.api.models import Question_Set, Matching_Point
from server.api.constants import LITTLE_QUESTION_SET_ID, BIG_QUESTION_SET_ID
from server.api.utils import send_all_event_emails, read_with_dropdown, q_set_json_to_array, paired_littles_to_array
#from server.api.matcher import generate_suggestions_for_bigs
from server.api.matcher import generate_suggestions_for_bigs, generate_suggestions_for
from werkzeug.utils import secure_filename
import xlrd
import json
import pandas as pd
import flask_excel as excel

admin_bp = Blueprint('admin', __name__)

#FIXME: test
@admin_bp.route("/admin")
@admin_bp.route("/admin/")
@limiter.limit("5 per second")
@login_required
@is_admin
def backend_index():
    big_submissions_cnt = Big_Answer.query.count()
    little_submissions_cnt = Little_Answer.query.count()

    return render_template('/admin/home.html', big_cnt=big_submissions_cnt,
                           little_cnt=little_submissions_cnt
                           )



#FIXME: test
@admin_bp.route("/admin/send_confirmation_email/little", methods=['GET', 'POST'])
@limiter.limit("2 per second")
@login_required
@is_admin
def send_confirmation_email_little():
    form = Send_Little_Email_Form()
    if form.validate_on_submit():
        recipient = form.email.data
        send_little_confirm_emails([recipient])
        flash("sent confirmation email to little")
        return redirect(url_for('admin.send_confirmation_email_little'))

    return render_template("/admin/test_send_email.html", form=form)


#FIXME: test
@admin_bp.route("/admin/send_confirmation_email/big", methods=['GET', 'POST'])
@limiter.limit("5 per second")
@login_required
@is_admin
def send_confirmation_email_big():
    form = Send_Big_Email_Form()
    if form.validate_on_submit():
        recipient = form.email.data
        send_big_confirm_emails([recipient])
        flash("sent confirmation email to big...")
        return redirect(url_for('admin.send_confirmation_email_big'))

    return render_template("/admin/test_send_email.html", form=form )


#send emails to everyone that are paired
@admin_bp.route("/admin/event/notify_all", methods=['GET', 'POST'])
@limiter.limit("2 per second")
@login_required
@is_admin
def notify_event():
    #form = Send_Big_Email_Form()
    form = Notify_Event_Form()
    if form.validate_on_submit():
        subject = form.subject.data
        email_body = form.event.data
        #send_big_confirm_emails([recipient])
        send_all_event_emails(subject=subject, email_content=email_body)

        flash("sent event emails...")
        return redirect(url_for('admin.notify_event'))

    return render_template("/admin/notify_event.html", form=form )



@admin_bp.route("/admin/confirmation_emaill/additional_message", methods=['GET', 'POST'])
@limiter.limit("2 per second")
@login_required
@is_admin
def confirmation_email_message():
    #form = Send_Big_Email_Form()
    form = Confirmation_Email_Form()
    db_record = Confirmation_Email_Message.query.first()
    if form.validate_on_submit():
        email_body = form.end_message.data
        if not db_record:
            new_confirmation_email_message = Confirmation_Email_Message(message=email_body)
            db.session.add(new_confirmation_email_message)
        else:
            db_record.message = email_body

        db.session.commit()
        flash("Updated the confirmation email additional message !")

        return redirect(url_for('admin.confirmation_email_message'))


    if db_record:
        form.end_message.data = db_record.message
    else:
        form.end_message.data = "There is no additional messages at the end of the confirmation emails!"


    return render_template("/admin/confirmation_email_additional_message.html", form=form )


#upload an excel file to update question set for big
@admin_bp.route('/admin/question_set/big/update', methods=['GET', 'POST'])
@limiter.limit('5 per second')
@login_required
@is_admin
def update_big_question_set():
    form = Upload_Question_Set_Form()

    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        print("---file name is: ", filename)
        #print("---file: ", f)

        #read the excel file to data frame
        data_xls = pd.read_excel(f)

        #drop the unanme columns
        data_xls.drop(data_xls.columns[data_xls.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

        #return the values in frist row
        categories = list(data_xls.columns)


        #print("--categories list: ", categories)
        question_size = len(data_xls)
        #print("--question size: ", question_size)

        excel_dict = data_xls.to_dict()
        weight_dict = excel_dict[categories[0]]
        #answer_list = excel_dict[categories[1]]
        question_dict = excel_dict[categories[2]]

        #print("----------weight list: ", weight_list)
        #print("----------question list: ", question_list)

        print("===============drop down ================")
        answers_list = read_with_dropdown(f)
        print("--drop down data: ", answers_list)

        big_questions_json = {}
        for q_idx in question_dict:
            q_idx = int(q_idx)
            type = "fr"

            if len(answers_list[q_idx]) > 1:
                type="mc"


            if type == "mc":
                big_questions_json[str(q_idx)] = {
                    'id': q_idx,
                    'weight': weight_dict[q_idx],
                    'type': type,
                    'question': question_dict[q_idx],
                    'answers': answers_list[q_idx]
                }

                #print("---in mc: ", answers_list[q_idx])
            else:
                big_questions_json[str(q_idx)] = {'id': q_idx,
                                             'weight': weight_dict[q_idx],
                                             'type': type,
                                             'question': question_dict[q_idx]
                }





        print("###END###")




        db_q_set = Big_Question_Set.query.first()
        big_html = data_xls.to_html()

        if not db_q_set:

            #store question json to the database
            db_q_set = Big_Question_Set(
                id = BIG_QUESTION_SET_ID,
                questions_json=big_questions_json,
                html=big_html
            )

            db.session.add(db_q_set)
            db.session.commit()

        else:
            #if question set already exist, update the json
            db_q_set.update_c(big_questions_json, big_html)



        #FIXME: checking
        #check_db_q_set = Question_Set.query.filter(Question_Set.id == BIG_QUESTION_SET_ID).first()
        #print("check db_q_set: ", check_db_q_set.get_json())
        #weight_list = data_xls.iloc[0, 1:]
        #num_rows = data_xls[data_xls.columns[0]].count()



        #return data_xls.to_html()
        flash("Question Set For Big Updated!!!")
        #return render_template("/admin/question_set_details.html", table=data_xls.to_html())
        return redirect(url_for('admin.big_question_set'))
        #return jsonify(data_xls.to_dict())


    return render_template("/admin/upload_question_set.html", form=form)


@admin_bp.route("/admin/question_set/big")
@limiter.limit("5 per second")
@login_required
@is_admin
def big_question_set():
    db_big_q_set = Big_Question_Set.query.first()
    html = ""
    if db_big_q_set:
        html = db_big_q_set.get_html()
        flash("Not all multiple question choices will be shown, please refer to the forms in front end for complete list!")
    else:
        flash("Big question set is not available, please upload one!")

    return render_template("/admin/question_set_details.html", table=html, type="Big")


#FIXME: change to submission later
#get all the big submission
@admin_bp.route('/admin/question_set/big/all_answers')
@limiter.limit("2 per second")
@login_required
@is_admin
def all_big_answers():
    temp_list = []

    #db_answers = Answer.query.filter(Answer.question_set_id == BIG_QUESTION_SET_ID).all()
    db_answers = Big_Answer.query.all()

    for one_set_answer in db_answers:
        temp_list.append(one_set_answer.get_json())

    print("temp list of big all answers: ", temp_list)


    #{'answers': [answers, answers, answers]}
    return {"answers": temp_list}



#get next or previous big submission depends on the flag and big id
@admin_bp.route('/admin/question_set/big/next_submission/<flag>/<previous_id>')
@limiter.limit("5 per second")
@login_required
@is_admin
def next_big_submission(flag, previous_id):
    try:
        if not previous_id:
            previous_id = -1
        else:
            previous_id = int(previous_id)
    except:
        return "Invalid previous_id", 400

    next_submission = None

    if(int(flag) > 0):
        next_submission = Big_Answer.query.filter(Big_Answer.is_paired==False).order_by(Big_Answer.id).filter(
                                              Big_Answer.id > previous_id
                                              ).first()
    elif (int(flag) < 0):
        next_submission = Big_Answer.query.filter(Big_Answer.is_paired==False).order_by(Big_Answer.id.desc()).filter(
                                              Big_Answer.id < previous_id
                                              ).first()


    if int(flag) == 0:
    #if int(flag) == 0 or not next_submission:
        next_submission = Big_Answer.query.filter(
                                              Big_Answer.id >= previous_id
                                              ).first()


    if not next_submission:
        raise 404

    current_id = next_submission.id
    json_result = next_submission.get_json()
    json_result['id'] = current_id

    #print("previous id: ",previous_id,"current id: ", current_id)

    #FIXME: may need for debug
    #print("---next big submission: json returned: ", json_result)
    #print("previous id: ", previous_id, " current id: ", current_id, "next submission: ", next_submission.get_json())
    return json_result




#upload and update question set for big
@admin_bp.route('/admin/question_set/little/update', methods=['GET', 'POST'])
@limiter.limit('5 per second')
@login_required
@is_admin
def update_little_question_set():
    form = Upload_Question_Set_Form()

    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        print("---file name is: ", filename)
        #print("---file: ", f)

        #read the excel file to data frame
        data_xls = pd.read_excel(f)

        #drop the unanme columns
        data_xls.drop(data_xls.columns[data_xls.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

        categories = list(data_xls.columns)


        question_size = len(data_xls)

        excel_dict = data_xls.to_dict()
        weight_dict = excel_dict[categories[0]]
        question_dict = excel_dict[categories[2]]


        print("===============drop down ================")
        answers_list = read_with_dropdown(f)

        little_questions_json = {}
        for q_idx in question_dict:
            q_idx = int(q_idx)
            type = "fr"

            if len(answers_list[q_idx]) > 1:
                type="mc"


            if type == "mc":
                little_questions_json[str(q_idx)] = {
                    'id': q_idx,
                    'weight': weight_dict[q_idx],
                    'type': type,
                    'question': question_dict[q_idx],
                    'answers': answers_list[q_idx]
                }

                #print("---in mc: ", answers_list[q_idx])
            else:
                little_questions_json[str(q_idx)] = {'id': q_idx,
                                                  'weight': weight_dict[q_idx],
                                                  'type': type,
                                                  'question': question_dict[q_idx]
                                                  }





        print("###END###")




        db_q_set = Little_Question_Set.query.first()
        little_html = data_xls.to_html()

        if not db_q_set:

            #store question json to the database
            db_q_set = Little_Question_Set(
                id = LITTLE_QUESTION_SET_ID,
                questions_json=little_questions_json,
                html=little_html
            )

            db.session.add(db_q_set)
            db.session.commit()

        else:
            #if question set already exist, update the json
            db_q_set.update_c(little_questions_json, little_html)



        #FIXME: checking
        #check_db_q_set = Question_Set.query.filter(Question_Set.id == BIG_QUESTION_SET_ID).first()
        #print("check db_q_set: ", check_db_q_set.get_json())
        #weight_list = data_xls.iloc[0, 1:]
        #num_rows = data_xls[data_xls.columns[0]].count()

        #return data_xls.to_html()
        #return jsonify(data_xls.to_dict())
        flash("Question Set for Little Updated!!!")
        #return render_template("/admin/question_set_updated.html", table=little_html)
        return redirect(url_for("admin.little_question_set"))


    return render_template("/admin/upload_question_set.html", form=form)

@admin_bp.route("/admin/question_set/little")
@limiter.limit("5 per second")
@login_required
@is_admin
def little_question_set():
    db_little_q_set = Little_Question_Set.query.first()
    html=""
    if db_little_q_set:
        html = db_little_q_set.get_html()
        flash("Not all multiple question choices will be shown, please refer to the forms in front end for complete list!")
    else:
        flash("Little question set is not available, please upload one!")

    return render_template("/admin/question_set_details.html", table=html, type="Little")

#get all the answers in terms of json for little submission
@admin_bp.route('/admin/question_set/little/all_answers')
@limiter.limit("5 per second")
@login_required
@is_admin
def all_little_answers():
    temp_list = []

    db_answers = Little_Answer.query.all()

    for one_set_answer in db_answers:
        temp_list.append(one_set_answer.get_json())


    #{'answers': [answers, answers, answers]}
    return {"answers": temp_list}


"""
#next or previous little submission depends on the flag
@admin_bp.route('/admin/question_set/little/next_submission/<flag>/<previous_id>')
@limiter.limit("5 per second")
def next_little_submission(flag, previous_id):
    try:
        if not previous_id:
            previous_id = -1
        else:
            previous_id = int(previous_id)
    except:
        return "Invalid previous id",400


    next_submission = None

    #print("----flag: ", flag, " previous id: ", previous_id)

    if(int(flag) > 0):
        next_submission = Little_Answer.query.filter(
                                              Little_Answer.id > previous_id
                                              ).first()
    elif (int(flag) < 0):
        next_submission = Little_Answer.query.order_by(Little_Answer.id.desc()).filter(
                                              Little_Answer.id < previous_id
                                              ).first()

    if int(flag) == 0 or not next_submission:
        next_submission = Little_Answer.query.filter(
                                              Little_Answer.id >= previous_id
                                              ).first()

    if not next_submission:
        raise 404


    current_id = next_submission.id
    json_result = next_submission.get_json()
    json_result['id'] = current_id

    print("--------current id of little clicked: ", current_id)

    #print("previous id: ", previous_id, " current id: ", current_id, "next submission: ", next_submission.get_json())
    return json_result
"""


@admin_bp.route('/admin/question_set/little/next_submission/<flag>/<previous_id>')
@limiter.limit("5 per second")
@login_required
@is_admin
def next_little_submission(flag, previous_id):
    try:
        if not previous_id:
            previous_id = -1
        else:
            previous_id = int(previous_id)
    except:
        return "Invalid previous id",400


    next_submission = None

    #print("----flag: ", flag, " previous id: ", previous_id)

    next_submission = Little_Answer.query.filter(
        Little_Answer.id >= previous_id
    ).first()

    if not next_submission:
        raise 404


    current_id = next_submission.id
    json_result = next_submission.get_json()
    json_result['id'] = current_id

    #print("previous id: ", previous_id, " current id: ", current_id, "next submission: ", next_submission.get_json())
    return json_result



#get the top choices for current big submission
@admin_bp.route("/admin/top_choices/<big_submission_id>")
@limiter.limit("5 per second")
@login_required
@is_admin
def big_top_choices(big_submission_id):
    big_submission_id = int(big_submission_id)

    #call helper function to get suggestions json
    suggestions_json = generate_suggestions_for(big_submission_id)

    suggestions_json['big_submission_id'] = big_submission_id

    return suggestions_json




@admin_bp.route("/admin/full_auto_matcher")
@admin_bp.route("/admin/full_auto_matcher/")
@limiter.limit("5 per second")
@login_required
@is_admin
def full_auto_matcher():
    db_big_submissions_cnt = Big_Answer.query.count()
    db_little_submissions_cnt = Little_Answer.query.count()

    if db_big_submissions_cnt == 0:
        flash("There is no big submission, this function may not work properly!")

    if db_little_submissions_cnt == 0:
        flash("There is no little submission, this function may not work properly!")

    return render_template("/admin/full_auto_grading_page.html")



@admin_bp.route("/admin/top_choices_html/<big_submission_id>")
@limiter.limit("5 per second")
@login_required
@is_admin
def big_top_choices_html(big_submission_id):
    big_submission_id = int(big_submission_id)

    suggestions_json = {}
    suggestions_json['suggestions'] = generate_suggestions_for(big_submission_id)

    suggestions_json["big_submission_id"] = big_submission_id

    return render_template("/admin/_suggestions.html", suggestions=suggestions_json, suggestions_json=json.dumps(suggestions_json))

@admin_bp.route("/admin/email_format/confirm_email/<big_id>")
@limiter.limit("5 per second")
@login_required
@is_admin
def get_confirm_email_format(big_id):
    print("------------here..")
    db_big_submission = Big_Answer.query.filter(Big_Answer.id == big_id).first()
    if (not db_big_submission) or (not db_big_submission.is_paired):
        flash("--send confirmation email failed, either big id not exist or not paired!")
        return "--send confirmation email failed, either big id not exist or not paired!"

    paired_littles= db_big_submission.paired_littles
    big_name = db_big_submission.name



    littles_json_list = []
    for one_little in paired_littles:
        littles_json_list.append(one_little.get_json())

    result_list = paired_littles_to_array(littles_json_list)



    return render_template("/emails/answers_table.html", result_list=result_list, name=big_name)

@admin_bp.route("/admin/confirm_and_notify/<big_id>")
@limiter.limit("5 per second")
@login_required
@is_admin
def confirm_and_notify(big_id):
    db_big_submission = Big_Answer.query.filter(Big_Answer.id == big_id).first()
    if (not db_big_submission) or (not db_big_submission.is_paired):
        flash("--send confirmation email failed, either big id not exist or not paired!")
        return "--send confirmation email failed, either big id not exist or not paired!"

    paired_littles= db_big_submission.paired_littles
    big_name = db_big_submission.name
    big_email = db_big_submission.email
    if not big_email:
        flash("Big submission doesn't have valid email!")
        return redirect(url_for('admin.show_unconfirmed_pairings')), 400

    little_emails = []

    print("--paired littles: ", paired_littles)

    littles_json_list = []
    for one_little in paired_littles:
        littles_json_list.append(one_little.get_json())
        one_little_email = one_little.email
        one_little_name = one_little.name
        one_little_id = one_little.id
        if not one_little_email:
            flash("One or more little submission doesn't have valid email!")
            return redirect(url_for('admin.show_unconfirmed_pairings')), 400
        little_emails.append([one_little_email, one_little_name, one_little_id])

    #for big
    result_list = paired_littles_to_array(littles_json_list)

    send_big_confirm_emails([big_email], name=big_name, result_list=result_list)
    db_big_submission.email_sent = True

    #FIXME: check this part later..
    for one_little_list in little_emails:
        one_little_resp = send_little_confirm_emails(email_list=[one_little_list[0]], name=one_little_list[1])



    for one_little in paired_littles:
        one_little.email_sent = True
    db.session.commit()


    return render_template("/emails/answers_table.html", result_list=result_list, name=big_name)

@admin_bp.route("/admin/confirm_pairing", methods=['POST'])
@limiter.limit("5 per second")
@login_required
@is_admin
def confirm_pairing():
    pairing_json = request.get_json()
    big_id = int(pairing_json['big_id'])
    del pairing_json['big_id']

    db_big = Big_Answer.query.filter(Big_Answer.id == big_id).first()

    if db_big.is_paired:
        return {"message":"", "error":"Error: can not have new pairs, already paired!"}

    print("--big id: ", big_id)

    for one_key in pairing_json:
        print("--one key: ", one_key)

        one_little_id = int(pairing_json[one_key])
        db_one_little = Little_Answer.query.filter(Little_Answer.id == one_little_id).first()
        print("--one little: ", db_one_little.name)

        db_one_little.big_id = big_id
        db_one_little.is_paired = True

    db_big.is_paired = True

    db.session.commit()


    return {"message": "Success: pair recoreded!!", "error":""}

@admin_bp.route("/admin/big/unpair_count")
@limiter.limit("5 per second")
@login_required
@is_admin
def big_unpair_count():
    db_big_unpair_cnt = Big_Answer.query.filter(Big_Answer.is_paired == False).count()
    return {"count": db_big_unpair_cnt}


@admin_bp.route("/admin/little/unpair_count")
@limiter.limit("5 per second")
@login_required
@is_admin
def little_unpair_count():
    db_little_unpair_cnt = Little_Answer.query.filter(Little_Answer.is_paired == False).count()
    return {"count": db_little_unpair_cnt}

@admin_bp.route("/admin/little/show_remaining")
@limiter.limit("5 per second")
@login_required
@is_admin
def little_show_remaining():
    db_little_unpair_remaining = Little_Answer.query.filter(Little_Answer.is_paired == False).all()
    #return {"count": db_little_unpair_cnt}

    idx = 0
    result_json = {}
    for one_little in db_little_unpair_remaining:
        one_little_info_json = {}
        one_little_info_json['id'] = one_little.id
        one_little_info_json['name'] = one_little.name
        one_little_info_json['age'] = one_little.age
        one_little_info_json['email'] = one_little.email
        one_little_info_json['email_sent'] = one_little.email_sent
        one_little_info_json['major_dept'] = one_little.major_dept
        one_little_info_json['major'] = one_little.major

        result_json[str(idx)] = one_little_info_json
        idx += 1


    return render_template("/admin/show_little_remaining.html", all_pairings_json=result_json)


#unpair the all littles from the big, unpair the big as well
@admin_bp.route("/admin/unpair_littles", methods=['POST'])
@limiter.limit("5 per second")
@login_required
@is_admin
def unpair_littles():
    pairings_json = request.get_json()

    for key in pairings_json:

        one_big_id = int(pairings_json[key])
        #del pairing_json['big_id']

        print("---unpairing... big id: ", one_big_id)

        db_big = Big_Answer.query.filter(Big_Answer.id == one_big_id).first()

        if not db_big.is_paired:
            continue

        print("--big id: ", one_big_id)

        littles = db_big.paired_littles

        for one_little in littles:
            print("--one little id: ", one_little.id)
            #FIXME: this will cause error in postgresql..
            #FIXME: may need a better way to disconnect them..
            #one_little.big_id = -1
            one_little.big_id = None
            one_little.is_paired = False

        db_big.is_paired = False

    db.session.commit()

    return {"message": "Success: unpaired succeefully!!", "error":""}



@admin_bp.route("/admin/show_confirmed_pairings")
@limiter.limit("5 per second")
@login_required
@is_admin
def show_confirmed_pairings():
    result_json = {}
    db_bigs = Big_Answer.query.filter(Big_Answer.is_paired == True,
                                      Big_Answer.email_sent == True
                                      ).order_by(Big_Answer.id.desc()).all()

    if not db_bigs:
        flash("The is no pairings available!")

    for one_big in db_bigs:
        combined_info_json = {}
        paired_littles_json = {}
        idx = 0
        for one_paired_little in one_big.paired_littles:
            #FIXME: add more details later..
            one_little_info_json = {}
            one_little_info_json['id'] = one_paired_little.id
            one_little_info_json['name'] = one_paired_little.name
            one_little_info_json['age'] = one_paired_little.age
            one_little_info_json['email'] = one_paired_little.email
            one_little_info_json['email_sent'] = one_paired_little.email_sent
            one_little_info_json['major_dept'] = one_paired_little.major_dept
            one_little_info_json['major'] = one_paired_little.major

            paired_littles_json[str(idx)] = one_little_info_json
            idx += 1

        #paired_littles_json['big_name'] = one_big.name
        #paired_littles_json['big_email_sent'] = one_big.email_sent

        combined_info_json['little_info'] =  paired_littles_json
        combined_info_json['big_info'] = {'name': one_big.name,
                                          'email': one_big.email,
                                          'email_sent': one_big.email_sent,
                                          'age': one_big.age,
                                          'major_dept': one_big.major_dept,
                                          'major': one_big.major
                                          }

        result_json[str(one_big.id)] = combined_info_json

    #{"big id": {'id': .., 'name'...}, 'big id': {}, ...}

    return render_template("/admin/show_confirmed_pairs.html", all_pairings_json=result_json)


#show all the big-little pairs
@admin_bp.route("/admin/show_unconfirmed_pairings")
@limiter.limit("5 per second")
@login_required
@is_admin
def show_unconfirmed_pairings():
    result_json = {}
    db_bigs = Big_Answer.query.filter(Big_Answer.is_paired == True,
                                      Big_Answer.email_sent == False
                                      ).order_by(Big_Answer.id.desc()).all()

    if not db_bigs:
        flash("The is no pairings available!")

    for one_big in db_bigs:
        combined_info_json = {}
        paired_littles_json = {}
        idx = 0
        for one_paired_little in one_big.paired_littles:
            #FIXME: add more details later..
            one_little_info_json = {}
            one_little_info_json['id'] = one_paired_little.id
            one_little_info_json['name'] = one_paired_little.name
            one_little_info_json['age'] = one_paired_little.age
            one_little_info_json['email'] = one_paired_little.email
            one_little_info_json['email_sent'] = one_paired_little.email_sent
            one_little_info_json['major_dept'] = one_paired_little.major_dept
            one_little_info_json['major'] = one_paired_little.major

            paired_littles_json[str(idx)] = one_little_info_json
            idx += 1

        #paired_littles_json['big_name'] = one_big.name
        #paired_littles_json['big_email_sent'] = one_big.email_sent

        combined_info_json['little_info'] =  paired_littles_json
        combined_info_json['big_info'] = {'name': one_big.name,
                                          'email': one_big.email,
                                          'email_sent': one_big.email_sent,
                                          'age': one_big.age,
                                          'major_dept': one_big.major_dept,
                                          'major': one_big.major
                                          }

        result_json[str(one_big.id)] = combined_info_json

    #{"big id": {'id': .., 'name'...}, 'big id': {}, ...}

    return render_template("/admin/show_unconfirmed_pairs.html", all_pairings_json=result_json)


#download big submissions
@admin_bp.route("/admin/download/big_submissions")
@limiter.limit("5 per second")
@login_required
@is_admin
def download_big_submissions():
    json_data = {}

    questions_list = []
    answers_list = []

    return_list = [[],[]]


    #use first question to get started
    db_first_big_submission = Big_Answer.query.first()
    one_json = db_first_big_submission.get_json()



    for temp_key in one_json:
        #the part that stored basic info in outter part, not question dict
        if not temp_key.isnumeric():
            continue
        one_q = one_json[temp_key]
        questions_list.append(one_q['question'])
        answers_list.append([one_q['answer']])

        #return_list.append([one_q['question'], one_q['answer']])
        return_list[0].append(one_q['question'])
        return_list[1].append(one_q['answer'])

    return_idx = 2

    db_big_submissions = Big_Answer.query.filter(Big_Answer.id > db_first_big_submission.id).all()

    for one_big_submission in db_big_submissions:
        one_big_json = one_big_submission.get_json()
        idx = 0
        for temp_key in one_big_json:
            # the part that stored basic info in outter part, not question dict
            if not temp_key.isnumeric():
                continue

            one_q = one_big_json[temp_key]
            answers_list[idx].append(one_q['answer'])

            if len(return_list) <= return_idx:
                return_list.append([one_q['answer']])
            else:
                return_list[return_idx].append(one_q['answer'])

            idx += 1

        return_idx += 1


    for idx in range(len(questions_list)):
        the_question = questions_list[idx]
        json_data[the_question] = answers_list[idx]

    return excel.make_response_from_array(return_list, "csv", file_name="big_submissions")




#download all responses from little as excel
@admin_bp.route("/admin/download/little_submissions")
@limiter.limit("5 per second")
@login_required
@is_admin
def download_little_submissions():
    #json_file = {"name": "bill", "age":21}

    json_data = {}

    questions_list = []
    answers_list = []

    return_list = [[],[]]

    #get the first little submission, use that as starting point
    db_first_little_submission = Little_Answer.query.first()
    one_json = db_first_little_submission.get_json()


    for temp_key in one_json:
        #the part that stored basic info in outter part, not question dict
        if not temp_key.isnumeric():
            continue
        one_q = one_json[temp_key]
        questions_list.append(one_q['question'])
        answers_list.append([one_q['answer']])

        #return_list.append([one_q['question'], one_q['answer']])
        return_list[0].append(one_q['question'])
        return_list[1].append(one_q['answer'])

    return_idx = 2

    db_little_submissions = Little_Answer.query.filter(Little_Answer.id > db_first_little_submission.id).all()

    for one_little_submission in db_little_submissions:
        one_little_json = one_little_submission.get_json()
        idx = 0
        for temp_key in one_little_json:
            # the part that stored basic info in outter part, not question dict
            if not temp_key.isnumeric():
                continue

            one_q = one_little_json[temp_key]
            answers_list[idx].append(one_q['answer'])

            if len(return_list) <= return_idx:
                return_list.append([one_q['answer']])
            else:
                return_list[return_idx].append(one_q['answer'])

            idx += 1

        return_idx += 1


    for idx in range(len(questions_list)):
        the_question = questions_list[idx]
        json_data[the_question] = answers_list[idx]

    return excel.make_response_from_array(return_list, "csv", file_name="little_submissions")




#download big question set as excel
@admin_bp.route("/admin/download/big_question_set")
@limiter.limit("5 per second")
@login_required
@is_admin
def download_big_question_set():
    #return_list = [[3,4,5], ["bill",["no1", "no2", "no3", "no4"],"jim"]]


    db_big_q_set = Big_Question_Set.query.first()
    db_q_json = db_big_q_set.get_json()
    return_list = q_set_json_to_array(db_q_json)

    return excel.make_response_from_array(return_list, "csv", file_name="backup_big_q_set")


#download little question set as excel
@admin_bp.route("/admin/download/little_question_set")
@limiter.limit("5 per second")
@login_required
@is_admin
def download_little_question_set():
    # return_list = [[3,4,5], ["bill",["no1", "no2", "no3", "no4"],"jim"]]

    db_little_q_set = Little_Question_Set.query.first()
    db_q_json = db_little_q_set.get_json()
    return_list = q_set_json_to_array(db_q_json)


    return excel.make_response_from_array(return_list, "csv", file_name="backup_little_q_set")
