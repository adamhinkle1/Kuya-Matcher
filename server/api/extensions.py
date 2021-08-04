#this file contains extensions for the backend part

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sendgrid import SendGridAPIClient
import os
from flask import redirect, url_for
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from faker import Faker
from flask_wtf.csrf import CSRFProtect

limiter = Limiter(key_func=get_remote_address, default_limits=["5 per second"])

#database
db = SQLAlchemy()


login_manager = LoginManager()

#this function will be called whenever check "login_required" decorator
@login_manager.user_loader
def load_user(user_id):
    #put it here to prevent recursive import with "models.py"
    from server.api.models import User
    user = User.query.get_or_404(user_id)
    return user



@login_manager.unauthorized_handler
def unauthorized():
    print("----failed login_required decorator...")
    return redirect(url_for('auth.access_denied'))


sendgrid_client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

moment = Moment()
bootstrap = Bootstrap()

gmail_client = Mail()

fake = Faker()

csrf = CSRFProtect()