from application.database import db
from datetime import datetime, timedelta

class User(db.Model):
    user_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    phone =  db.Column(db.String(50),nullable=False,unique=True)
    email =  db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False,unique=True)
    address = db.Column(db.String(50),nullable=True,unique=False)
    role = db.Column(db.String(50),nullable=False,default='customer')

    def __init__(self,name,phone,email,password,address,role):
        self.name=name
        self.phone=phone
        self.email=email
        self.password=password
        self.address=address
        self.role=role

    def __repr__(self):
        return f'<User {self.user_id}>'

    def to_dict(self):
        return {
            'user_id':self.user_id,
            'name':self.name,
            'phone':self.phone,
            'email':self.email,
            'password':self.password,
            'address':self.address,
            'role':self.role
        }

class Section(db.Model):
    section_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self,name,description,date_created):
        self.name=name
        self.description=description
        self.date_created=date_created

    def __repr__(self):
        return '<section %r>' % self.name

    def to_dict(self):
        return {
            'section_id':self.section_id,
            'name':self.name,
            'description':self.description,
            'date_created':self.date_created
        }


# class author(db.Model):
#     author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
    
#     def __repr__(self):
#         return '<author %r>' % self.name

# class publisher(db.Model):
#     publisher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
    
#     def __repr__(self):
#         return '<publisher %r>' % self.name

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    section_name = db.Column(db.String(80), nullable=False)
    author_name = db.Column(db.String(80),  nullable=False)
    publisher_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    keywords = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self,name,section_name,author_name,publisher_name,description,date_created,price,keywords):
        self.name=name
        self.section_name=section_name
        self.author_name=author_name
        self.publisher_name=publisher_name
        self.description=description
        self.date_created=date_created
        self.price=price
        self.keywords=keywords

    def __repr__(self):
        return '<book %r>' % self.name

    def to_dict(self):
        return {
            'book_id':self.book_id,
            'name':self.name,
            'section_name':self.section_name,
            'author_name':self.author_name,
            'publisher_name':self.publisher_name,
            'description':self.description,
            'date_created':self.date_created,
            'price':self.price,
            'keywords':self.keywords
        }

class issued_book(db.Model):
    issue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False, default= issue_date + timedelta(days=7))

    def to_dict(self):
        return {
            'issue_id':self.issue_id,
            'user_id':self.user_id,
            'book_id':self.book_id,
            'issue_date':self.issue_date,
            'return_date':self.return_date
        }

class requested_book(db.Model):
    req_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False)


    def to_dict(self):
        return {
            'req_id':self.req_id,
            'user_id':self.user_id,
            'book_id':self.book_id,
            'request_date':self.request_date
        }

class UserRecord(db.Model):
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False, default= issue_date + timedelta(days=7))

    def to_dict(self):
        return {
            'record_id':self.record_id,
            'user_id':self.user_id,
            'book_id':self.book_id,
            'issue_date':self.issue_date,
            'return_date':self.return_date
        }

class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    feedback = db.Column(db.String(250), unique=True, nullable=False)

    def to_dict(self):
        return {
            'feedback_id':self.feedback_id,
            'user_id':self.user_id,
            'book_id':self.book_id,
            'feedback':self.feedback
        }
