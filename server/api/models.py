from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from server.api.extensions import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.String(30), primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    email_verified = db.Column(db.Boolean, default=False)
    json_info = db.Column(JSON)

    is_admin = db.Column(db.Boolean, default=False)


    def get_json(self):
        return self.json_info




#FIXME: need more work when we need to make it to multiple choice
class Big_Question_Set(db.Model):
    __tablename__ = 'big_question_set'
    #current id for little: "000", big: "111"
    #id = db.Column(db.String(3), primary_key=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    #{"questions":[{"....":[possible answers]}, {"....":[possible_answers]}, "{....: [possible_answers]}"]}
    questions_json = db.Column(JSON)
    html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def get_json(self):
        return self.questions_json

    def get_html(self):
        return self.html

    #one to many relationship
    #answers = db.relationship('Answer', back_populates='the_question_set', cascade='all, delete-orphan')
    answers = db.relationship('Big_Answer', back_populates='the_question_set', cascade='all, delete-orphan')

    #with commit
    def update_c(self, new_json, new_html):
        self.questions_json = new_json
        self.html = new_html
        db.session.commit()

"""
class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)

    #{"answers":["...", "...", "..."]}
    answers_json = db.Column(JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    #email = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(30))

    #flag to keep track whether the respondent is paired or not
    is_paired = db.Column(db.Boolean, default=False)
    email_sent = db.Column(db.Boolean, default=False)

    #FIXME
    #refer back to question set
    #question_set_id = db.Column(db.String(30), db.ForeignKey('question_set.id'))
    #the_question_set = db.relationship('Question_Set', back_populates='answers')


    def get_json(self):
        return self.answers_json
"""

class Big_Answer(db.Model):
    __tablename__ = 'big_answer'
    id = db.Column(db.Integer, primary_key=True)

    #{"answers":["...", "...", "..."]}
    answers_json = db.Column(JSON)
    #timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    #email = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    age = db.Column(db.String(5))
    major_dept = db.Column(db.String(50))
    major = db.Column(db.String(50))

    #suggested_littles_json = db.Column(MutableDict.as_mutable(JSON), default={})
    #{'0': {'point': the point, 'id': little id}, '1': {'point': the point, 'id': little id} }
    suggested_littles_json = db.Column(JSON)

    #flag to keep track whether the respondent is paired or not
    is_paired = db.Column(db.Boolean, default=False)
    #FIXME: I don't really want to delete the children when parent is deleted, will recheck later
    paired_littles = db.relationship('Little_Answer', back_populates='paired_big', cascade='all, delete-orphan')

    email_sent = db.Column(db.Boolean, default=False)

    #refer back to question set
    question_set_id = db.Column(db.Integer, db.ForeignKey('big_question_set.id'))
    the_question_set = db.relationship('Big_Question_Set', back_populates='answers')


    def get_json(self):
        return self.answers_json

    def get_suggestions_json(self):
        return self.suggested_littles_json



class Little_Question_Set(db.Model):
    __tablename__ = 'little_question_set'
    id = db.Column(db.Integer, primary_key=True)


    #{"questions":[{"....":[possible answers]}, {"....":[possible_answers]}, "{....: [possible_answers]}"]}
    questions_json = db.Column(JSON)
    html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def get_json(self):
        return self.questions_json

    def get_html(self):
        return self.html

    #one to many relationship
    #answers = db.relationship('Answer', back_populates='the_question_set', cascade='all, delete-orphan')
    answers = db.relationship('Little_Answer', back_populates='the_question_set', cascade='all, delete-orphan')

    #with commit
    def update_c(self, new_json, new_html):
        self.questions_json = new_json
        self.html = new_html
        db.session.commit()

class Little_Answer(db.Model):
    __tablename__ = 'little_answer'
    id = db.Column(db.Integer, primary_key=True)


    #{"answers":["...", "...", "..."]}
    answers_json = db.Column(JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    #email = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    age = db.Column(db.String(5))
    major_dept = db.Column(db.String(50))
    major = db.Column(db.String(50))

    #flag to keep track whether the respondent is paired or not
    is_paired = db.Column(db.Boolean, default=False)
    email_sent = db.Column(db.Boolean, default=False)

    big_id = db.Column(db.Integer, db.ForeignKey('big_answer.id'))
    paired_big = db.relationship('Big_Answer', back_populates='paired_littles')

    #refer back to question set
    question_set_id = db.Column(db.Integer, db.ForeignKey('little_question_set.id'))
    the_question_set = db.relationship('Little_Question_Set', back_populates='answers')

    def get_json(self):
        return self.answers_json





class Big_Little_Question_Pair(db.Model):
    __tablename__ = 'big_little_question_pair'
    id = db.Column(db.Integer, primary_key=True)
    #big_q = db.Column(db.String(100), nullable=False)
    #big_weight = db.Column(db.Integer, nullable=False)
    little_q_id = db.Column(db.Integer, nullable=False)

    #little_q = db.Column(db.String(100), nullable=False)
    #little_weight = db.Column(db.Integer, nullable=False)
    big_q_id = db.Column(db.Integer, nullable=False)

    total_weight = db.Column(db.Integer, nullable=False)
"""
"""

#store the point the different matches (big and little)
class Matching_Point(db.Model):
    __tablename__ = 'matching_point'
    id = db.Column(db.Integer, primary_key=True)
    #question_set_id = db.Column(db.String(30), nullable=False)
    big_answer_id = db.Column(db.Integer, nullable=False)
    little_answer_id = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Integer, default=0, index=True)


class Confirmation_Email_Message(db.Model):
    __tablename__ = 'confirmation_email_message'
    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.String(2000))
