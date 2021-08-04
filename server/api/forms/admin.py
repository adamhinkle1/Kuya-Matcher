from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, Email
from flask_ckeditor import CKEditorField


class Send_Little_Email_Form(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(3,30), Email()])
    submit = SubmitField('Send Little Email')

class Send_Big_Email_Form(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(3,30), Email()])
    submit = SubmitField('Send Big Email')

class Notify_Event_Form(FlaskForm):
    #email = StringField('email', validators=[DataRequired(), Length(3,1000)])
    subject = CKEditorField('subject', validators=[DataRequired(), Length(5, 1000)])
    event = CKEditorField('event', validators=[DataRequired(), Length(5, 10000)])
    submit = SubmitField('Notify Everyone')

class Confirmation_Email_Form(FlaskForm):
    #begin_message = CKEditorField('', validators=[DataRequired(), Length(5, 3000)])
    end_message = CKEditorField('', validators=[DataRequired(), Length(5, 10000)])
    submit = SubmitField('Update Additional Message')

class Upload_Result_Form(FlaskForm):
    file = FileField('file', validators=[FileRequired(),
                                        FileAllowed(['xlsx', 'csv'], 'Only files end with "xlsx" or "csv"')
                                        ])

    submit = SubmitField("Upload")

class Upload_Question_Set_Form(FlaskForm):
    file = FileField('file', validators=[FileRequired(),
                                         FileAllowed(['xlsx', 'csv'], 'Only files end with "xlsx" or "csv"')
                                         ])


    submit = SubmitField("Upload")
