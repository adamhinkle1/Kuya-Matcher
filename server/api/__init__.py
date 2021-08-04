from flask import Flask
from flask_login import current_user
import os
import click
import flask_excel as excel
#from server.api.extensions import limiter, db, login_manager, moment, bootstrap, gmail_client, csrf
from server.api.extensions import limiter, db, login_manager, moment, bootstrap, gmail_client
from server.api.blueprints.main import main_bp
from server.api.blueprints.auth import auth_bp
from server.api.blueprints.board_member import board_member_bp
from server.api.blueprints.user import user_bp
from server.api.blueprints.admin import admin_bp
from server.api.settings import website_config
from server.api.models import User

def create_app(config_name='production'):
    print("----config name: ", config_name)

    #app = Flask('api', static_folder='build', static_url_path='/')
    app = Flask('api', static_folder='build', static_url_path='/', template_folder='server/api/templates')


    #load configurations
    app.config.from_object(website_config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_error_handler(app)
    register_command(app)

    return app

def register_error_handler(app):
    # return this error code if user exceed the rate limit
    @app.errorhandler(429)
    def rate_limit_reached(e):
        return "your rate limited reached.. 429 ... Change me in api.__init__ file", 429

    # no permission error

    @app.errorhandler(403)
    def permission_denied(e):
        return "You don't have the permission.. 403", 403


    #when path not in backend, check frontend
    #FIXME: frontend need to take care of 404 error if it does not have the page either
    @app.errorhandler(404)
    def route_to_frontend(e):
        print("------404: ", e)
        return app.send_static_file('index.html')


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, prefix="/auth")
    app.register_blueprint(board_member_bp, prefix="/board_member")
    app.register_blueprint(user_bp, prefix="/user")
    app.register_blueprint(admin_bp, prefix="/admin")

def register_extensions(app):
    limiter.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    gmail_client.init_app(app)
    excel.init_excel(app)
    #csrf.init_app(app)
    #ckeditor.init_app(app)


def register_command(app):
    #in cmd, run:  flask test
    @app.cli.command()
    def test():
        click.echo("this is testing command")

    #command to initialize database, use will care...
    @app.cli.command()
    @click.option("--drop", is_flag=True, help="drop the tables")
    def init_db(drop):
        if drop:
            click.confirm("this will drop all the tables, are you sure? ", abort=True)
            #do not delete, if drop_all() failed, uncomment one of them to see if it works
            #db.reflect()
            #db.session.commit()
            db.drop_all()
            print("---dropped all tables")

        #recreate all the tables (empty)
        db.create_all()
        print("--created all tables")

        """

        #FIXME: add some prefined rows, delete later
        from server.api.constants import LITTLE_QUESTION_SET_ID, BIG_QUESTION_SET_ID
        from server.api.sample_big_question_set import SAMPLE_BIG_QUESTION_SET
        from server.api.sample_little_question_set import SAMPLE_LITTLE_QUESTION_SET
        from server.api.models import Question_Set

        new_little_q_set = Question_Set(id=LITTLE_QUESTION_SET_ID,
                                        questions_json=SAMPLE_LITTLE_QUESTION_SET
                                        )
        db.session.add(new_little_q_set)

        new_big_q_set = Question_Set(id=BIG_QUESTION_SET_ID,
                                     questions_json=SAMPLE_BIG_QUESTION_SET
                                     )
        db.session.add(new_big_q_set)

        db.session.commit()

        print("--added sample question_sets")
        """

    """
    @app.cli.command()
    def init_question_sets():
        from server.api.utils import generate_questions_responses
        generate_questions_responses(5)
        print("--------generated sample questions and responses")

    @app.cli.command()
    def show_points():
        from server.api.models import Matching_Point
        #db_matching_pts = Matching_Point.query.order_by(Matching_Point.point.desc()).all()
        db_matching_pts = Matching_Point.query.all()

        print("--------matching points------------")
        for one_matching_pt in db_matching_pts:
            print("id: ", one_matching_pt.id,"Point: ", one_matching_pt.point, ", big id: ", one_matching_pt.big_answer_id, " ,little id: ", one_matching_pt.little_answer_id)

        print("=========End=====================")

    """

    @app.cli.command()
    def init_submissions():
        click.confirm("this will drop the submissions from bigs and littles, are you sure? ", abort=True)
        from server.api.models import Big_Answer, Little_Answer

        #FIXME: cause error, because the fk for big is -1 if it's unpaired
        Little_Answer.query.delete()
        #the order matters here, don't change them!!
        Big_Answer.query.delete()
        db.session.commit()

        print("----all submissions from bigs and littles are deleted!")

    @app.cli.command()
    @click.argument("email")
    def add_admin(email):
        db_user = User.query.filter(User.email==email).first()
        if not db_user:
            print("--no user found with email: ", email, " ,please login once before assigning as an admin...")
            return

        if db_user.is_admin:
            print("--user is already an admin: ", email)
            return

        db_user.is_admin = True
        db.session.commit()
        print("--upgrade user with email: ", email, " to admin!!")

    @app.cli.command()
    @click.argument("email")
    def remove_admin(email):
        db_user = User.query.filter(User.email==email).first()
        if not db_user:
            print("--no user found with email: ", email)
            return

        if not db_user.is_admin:
            print("--user is not admin!! ", email)
            return

        #else:
        db_user.is_admin = False
        db.session.commit()
        print("removed admin: ", email)

    @app.cli.command()
    def all_admins():
        db_users = User.query.filter(User.is_admin==True).all()
        print("---Admins---")
        for one_admin in db_users:
            print("--User name: ", one_admin.name, ", user email: ", one_admin.email)
        print("###END###")








if __name__ == "__main__":
    app = create_app()
    #PORT is given by heroku, not necessary 5000
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
