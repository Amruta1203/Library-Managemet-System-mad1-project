from datetime import datetime
from flask_restful import Resource
from flask_restful import reqparse
from application.models import *
from flask import redirect,url_for,render_template,jsonify


class AddSection(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True)
        parser.add_argument('description',type=str,required=True)
        parser.add_argument('date',type=str,required=True)
        args = parser.parse_args()
        name = args['name']
        description = args['description']
        date = args['date']
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        section = Section(name,description,date_obj)
        db.session.add(section)
        db.session.commit()
        response = {'message':'section added successfully'}
        return response,200


class AddBook(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True)
        parser.add_argument('section',type=str,required=True)
        parser.add_argument('description',type=str,required=True)
        parser.add_argument('author',type=str,required=True)
        parser.add_argument('publisher',type=str,required=True)
        parser.add_argument('date',type=str,required=True)
        parser.add_argument('price',type=str,required=True)
        parser.add_argument('keywords',type=str,required=True)
        args = parser.parse_args()
        name = args['name']
        section = args['section']
        description = args['description']
        author = args['author']
        publisher = args['publisher']
        date = args['date']
        price = args['price']
        keywords = args['keywords']
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        book = Book(name,section,author,publisher,description,date_obj,price,keywords)
        db.session.add(book)
        db.session.commit()
        response = {'message':'book added successfully'}
        return response,200

class DeleteSection(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('section_id',type=str,required=True)
        args = parser.parse_args()
        section_id = args['section_id']
        section = Section.query.filter_by(section_id=section_id).first()
        db.session.delete(section)
        db.session.commit()
        response = {'message':'section deleted successfully'}
        return response,200

class DeleteBook(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_id',type=str,required=True)
        args = parser.parse_args()
        book_id = args['book_id']
        book = Book.query.filter_by(book_id=book_id).first()
        db.session.delete(book)
        db.session.commit()
        response = {'message':'book deleted successfully'}
        return response,200

class EditBook(Resource):
    def post(self,book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True)
        parser.add_argument('section',type=str,required=True)
        parser.add_argument('description',type=str,required=True)
        parser.add_argument('author',type=str,required=True)
        parser.add_argument('publisher',type=str,required=True)
        parser.add_argument('date',type=str,required=True)
        parser.add_argument('price',type=str,required=True)
        parser.add_argument('keywords',type=str,required=True)
        args = parser.parse_args()
        name = args['name']
        section = args['section']
        description = args['description']
        author = args['author']
        publisher = args['publisher']
        date = args['date']
        price = args['price']
        keywords = args['keywords']
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        book = Book.query.filter_by(book_id=book_id).first()
        book.name = name
        book.section = section
        book.description = description
        book.author = author
        book.publisher = publisher
        book.date = date_obj
        book.price = price
        book.keywords = keywords
        db.session.commit()
        response = {'message':'book updated successfully'}
        return response,200

class EditSection(Resource):
    def post(self,section_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True)
        parser.add_argument('description',type=str,required=True)
        parser.add_argument('date',type=str,required=True)
        args = parser.parse_args()
        name = args['name']
        description = args['description']
        date = args['date']
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        section = Section.query.filter_by(section_id=section_id).first()
        section.name = name
        section.description = description
        section.date = date_obj
        db.session.commit()
        response = {'message':'section updated successfully'}
        return response,200




   

        



