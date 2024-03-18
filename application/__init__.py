from flask import render_template,Flask
from application.database import db
from application.models import *
from flask_restful import Api
from application.api import *

app = Flask(__name__,template_folder='../templates',static_folder='../static')
app.config['secret_key']="abcdefgh"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3'
app.secret_key = 'secret key'

db.init_app(app)
api = Api(app)

api.add_resource(AddSection, '/api/add_section')
api.add_resource(AddBook, '/api/add_book')
api.add_resource(DeleteSection, '/api/delete_section')
api.add_resource(DeleteBook, '/api/delete_book')
api.add_resource(EditBook, '/api/edit_book/<book_id>')
api.add_resource(EditSection, '/api/edit_section/<section_id>')


# def create_admin():
#     user = User.query.filter_by(role='admin').first()
#     if user:
#         return
#     admin = User(name='admin',email='admin@gmail.com',password='admin@123',role='admin',phone='1234567890',address='library')
#     db.session.add(admin)
#     db.session.commit()





with app.app_context():
    #create_admin()
    db.create_all()
