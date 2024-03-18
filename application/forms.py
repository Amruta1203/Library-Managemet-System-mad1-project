# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    name = StringField('Book Name')
    author = StringField('Author')
    section = StringField('Section')
    submit = SubmitField('Search')

class FeedbackForm(FlaskForm):
    book_id = StringField('Book ID')
    user_id = StringField('User ID')
    book_name = StringField('Book Name')
    feedback = StringField('Feedback')
    submit = SubmitField('Submit')


