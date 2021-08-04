from flask import Blueprint, session, redirect, request, url_for
from flask_login import login_user , login_required, logout_user
from server.api.extensions import limiter, db
from server.api.utils import get_google_provider_cfg, google_client, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from server.api.models import User
import requests
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/auth/logout")
@login_required
def logout():
    #FIXME: temp, may need to logout the google as well, check the documentation
    logout_user()

    return redirect("/")

@auth_bp.route("/auth/login")
@limiter.limit("2 per second")
def login():
    #https://realpython.com/flask-google-login/
    #FIXME: research on how to login using google..
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for('auth.redirect_page', _external=True),
        scope=['openid','email','profile']
    )

    return redirect(request_uri)



@auth_bp.route("/auth/redirect")
def redirect_page():
    authorization_code = request.args.get('code')

    #find out what url to call to get tokens that allow we to ask things on behalf of user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    #prepare and send a request to get tokens
    token_url, headers, body = google_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=authorization_code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    #parse the token, now we have the token
    google_client.parse_request_body_response(json.dumps(token_response.json()))

    #get user info in term of json with token
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = google_client.add_token(userinfo_endpoint)
    userinfo_response_json = requests.get(uri, headers=headers, data=body).json()

    print("---userinfo response json: ", userinfo_response_json)


    #if userinfo_response.json().get('email_verified'):
    unique_id = userinfo_response_json['sub']
    user_email = userinfo_response_json['email']
    user_name = userinfo_response_json['given_name']
    #user_picture_url = userinfo_response_json['picture']
    email_verified = userinfo_response_json['email_verified']

    print("----id: ", unique_id, " ,user email: ", user_email, " , username : ", user_name)
    db_user = User.query.filter(User.id == unique_id).first()
    if not db_user:
        db_user = User(id=unique_id, email=user_email,
                       name=user_name, email_verified=email_verified,
                       json_info={'user': userinfo_response_json}
                       )
        db.session.add(db_user)
        db.session.commit()



    login_user(db_user)

    return redirect(url_for('main.index'))




@auth_bp.route("/auth/access_denied")
def access_denied():
    #supposedly, this should redirect to the login page
    return redirect("/", 403)


