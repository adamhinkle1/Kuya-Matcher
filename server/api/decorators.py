from functools import wraps
from flask_login import current_user
from flask import url_for, redirect
from server.api.models import User

# this file contains all kinds of decorators we are going to use
#--decorator: check if user is admin
def is_admin(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        # print("-------current session: ", session)
        # if logged_in value not exist or false, then user is not logged in
        try:
            if not current_user.is_admin:
                return redirect(url_for('auth.access_denied'))
        except Exception as e:
            print("---------is_admin decorator Exception: ", e)

            return redirect(url_for('auth.access_denied'))

        return func(*args, **kwargs)

    return decorated_function
