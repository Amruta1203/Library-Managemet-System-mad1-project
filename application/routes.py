import matplotlib
matplotlib.use('Agg')
from application import app
from application.models import *
from application.database import db
from application.forms import *
from flask import render_template,request,redirect,url_for,session,flash,send_file
from datetime import datetime,date
from sqlalchemy import join
from sqlalchemy import create_engine, text
import requests
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
import base64


@app.route('/')
def default():
    all_books=issued_book.query.all()
    print(all_books)
    today_date=datetime.today()
    for i in all_books:
        if i.return_date <= today_date:
            db.session.delete(i)
            db.session.commit()
    return render_template('default.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        user = User(name,phone,email,password,address,'customer')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user'] = user.to_dict()
            if session.get('user')['role'] == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('user_stats'))
    return render_template('login.html')

@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user'] = user.to_dict()
            if session.get('user')['role'] == 'admin':
                return redirect(url_for('index'))
                
            return redirect(url_for('user'))
    return render_template('admin_login.html')

@app.route('/user')
def user():
    if session.get('user'):
        return render_template('user_dash.html',user=session.get('user'))
    return redirect(url_for('login'))

# @app.route('/admin')
# def admin():
#     if not session.get('user'):
#         return redirect(url_for('login'))
#     if session.get('user')['role'] != 'admin':
#         return redirect(url_for('login'))
  
#     return render_template('admin_dash.html',requests=requested_book.query.all())

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

@app.route('/add_section',methods=['GET','POST'])
def add_section():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/api/add_section'
        data = {
            'name':request.form['name'],
            'description':request.form['description'],
            'date':request.form['date']
        }
        r = requests.post(url,json=data,verify=False)
        print(r.text)
        if r.status_code == 200:
            result=r.json()
            print(result['message'])
        return redirect(url_for('admin'))
    return render_template('add_section.html')


@app.route('/add_book',methods=['GET','POST'])
def add_book():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/api/add_book'
        data = {
            'name':request.form['name'],
            'section':request.form['section'],
            'description':request.form['description'],
            'author':request.form['author'],
            'publisher':request.form['publisher'],
            'date':request.form['date'],
            'price':request.form['price'],
            'keywords':request.form['keywords']

        }
        r = requests.post(url,json=data,verify=False)
        print(r.text)
        if r.status_code == 200:
            result=r.json()
            print(result['message'])
        return redirect(url_for('admin'))
    return render_template('add_book.html')

@app.route('/view_books',methods=['GET','POST'])
def view_books():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    books = Book.query.all()
    return render_template('view_books.html',books=books)

        
@app.route('/view_section',methods=['GET','POST'])
def view_section():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    sections = Section.query.all()
    return render_template('view_section.html',sections=sections)

@app.route('/Books',methods=['GET','POST'])
def Books():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    books = Book.query.all()
    return render_template('Books.html',books=books)

@app.route('/delete_section',methods=['GET','POST'])
def delete_section():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/api/delete_section'
        data = {
            'section_id':request.form['section_id']
        }
        r = requests.post(url,json=data,verify=False)
        print(r.text)
        if r.status_code == 200:
            result=r.json()
            print(result['message'])
        return redirect(url_for('delete_section'))
    return render_template('delete_section.html',sections=Section.query.all())

@app.route('/delete_book',methods=['GET','POST'])
def delete_book():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/api/delete_book'
        data = {
            'book_id':request.form['book_id']
        }
        r = requests.post(url,json=data,verify=False)
        print(r.text)
        if r.status_code == 200:
            result=r.json()
            print(result['message'])
        return redirect(url_for('delete_book'))
    return render_template('delete_book.html',books=Book.query.all())

#testing edit section
@app.route('/edit_section/get',methods=['GET','POST'])
def edit_section_get():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    sections=Section.query.all()
    return render_template('edit_section_get.html',sections=sections)

@app.route('/edit_section/<section_id>',methods=['GET','POST'])
def edit_section(section_id):
    section = Section.query.get_or_404(section_id)
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        # section.name = request.form['name']
        # section.description = request.form['description']
        # db.session.commit()
        url = 'http://127.0.0.1:5000/api/edit_section/'+section_id
        data = {
            'section_id':section_id,
            'name':request.form['name'],
            'description':request.form['description'],
            'date':request.form['date']
        }
        r = requests.post(url,json=data,verify=False)
        print(r.text)
        if r.status_code == 200:
            result=r.json()
            print(result['message'])
        return redirect(url_for('edit_section_get'))
    return render_template('edit_section.html',sections=section)

  
@app.route('/edit_book/get',methods=['GET','POST'])
def edit_book_get():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    books=Book.query.all()
    return render_template('edit_book_get.html',books=books)

@app.route('/edit_book/<book_id>',methods=['GET','POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/api/edit_book/'+book_id
        data = {
            'book_id':book_id,
            'name':request.form['name'],
            'section':request.form['section'],
            'author':request.form['author'],
            'publisher':request.form['publisher'],
            'description':request.form['description'],
            'price':request.form['price'],
            'keywords':request.form['keywords'],
            'date':request.form['date']
        }
        r = requests.post(url,json=data,verify=False)
        print(r.text)
        if r.status_code == 200:
            result=r.json()
            print(result['message'])
        return redirect(url_for('edit_book_get'))
    return render_template('edit_book.html',books=book)
@app.route('/request_book',methods=['GET','POST'])
def request_book():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session.get('user')['user_id']
        book_id = request.form['book_id']
        issue_date = datetime.now()
        user_count = requested_book.query.filter_by(user_id=user_id).count()
        
        if user_count<5:
            if requested_book.query.filter_by(user_id=user_id,book_id=book_id).first():
                flash('Already requested')
                return redirect(url_for('Books'))
            else:
                requested = requested_book(user_id=user_id,book_id=book_id,request_date=issue_date)
                db.session.add(requested)
                db.session.commit()
        
    return redirect(url_for('Books'))

@app.route('/issue_books',methods=['GET','POST'])
def issue_books():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        req_id = request.form['req_id']
        user_id = request.form['user_id']
        book_id = request.form['book_id']
        issue_date = datetime.now()
        return_date = issue_date + timedelta(days=7)
        if issued_book.query.filter_by(user_id=user_id,book_id=book_id).first():
            flash('Already issued')
            return redirect(url_for('admin'))
        if issued_book.query.filter_by(user_id=user_id).count()>4:
            print('already issued 5 books')
            flash('Already issued 5 books')
        else:
            issued = issued_book(user_id=user_id,book_id=book_id,issue_date=issue_date,return_date=return_date)
            recorded = UserRecord(user_id=user_id,book_id=book_id,issue_date=issue_date,return_date=return_date)
            db.session.add(issued)
            db.session.add(recorded)
            db.session.delete(requested_book.query.filter_by(req_id=req_id).first())
            db.session.commit()
        return redirect(url_for('issue_books'))
    req_info = db.session.query(requested_book,Book).join(Book,requested_book.book_id==Book.book_id).all()
    return render_template('requests.html',requests=req_info)

@app.route('/revoke_books',methods=['GET','POST'])
def revoke_books():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        issue_id = request.form['issue_id']
        db.session.delete(issued_book.query.filter_by(issue_id=issue_id).first())
        db.session.commit()
        return redirect(url_for('revoke_books'))
    issue_info = db.session.query(issued_book,Book).join(Book,issued_book.book_id==Book.book_id).all()
    return render_template('revoke.html',issues=issue_info)

@app.route('/MyBooks',methods=['GET','POST'])
def MyBooks():
    user_id = session.get('user')['user_id']
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    Mybook_info = db.session.query(UserRecord,Book).join(Book,UserRecord.book_id==Book.book_id).filter(UserRecord.user_id==user_id).all()
    return render_template('MyBooks.html',records=Mybook_info)

@app.route('/view_section_user',methods=['GET','POST'])
def view_section_user():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    return render_template('view_section_user.html',sections=Section.query.all())
    
@app.route('/search',methods=['GET','POST'])
def search():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    form=SearchForm()
    if form.validate_on_submit():
        name = form.name.data
        books=Book.query.filter(Book.name.like('%'+name+'%')).all()
        return render_template('searchByName.html',books=books,form=form)
    return render_template('searchByName.html',form=form)

@app.route('/searchByAuthor',methods=['GET','POST'])
def searchByAuthor():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    form=SearchForm()
    if form.validate_on_submit():
        author = form.author.data
        books=Book.query.filter(Book.author_name.like('%'+author+'%')).all()
        return render_template('searchByauthor.html',books=books,form=form)
    return render_template('searchByauthor.html',form=form)

@app.route('/searchBySection',methods=['GET','POST'])
def searchBySection():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    form=SearchForm()
    if form.validate_on_submit():
        section = form.section.data
        books=Book.query.filter(Book.section_name.like('%'+section+'%')).all()  
        return render_template('searchBySection.html',books=books,form=form)
    return render_template('searchBySection.html',form=form)


@app.route('/feedback/<user_id>/<book_id>',methods=['GET','POST'])
def feedback(user_id,book_id):
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    form=FeedbackForm()
    book_name = Book.query.filter_by(book_id=book_id).first().name
    if form.validate_on_submit():
        user_id = form.user_id.data
        book_id = form.book_id.data
        print("form validated")
        feedback = form.feedback.data
        feedback = Feedback(book_id=book_id,feedback=feedback,user_id=user_id)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('MyBooks'))
    return render_template('feedback.html',form=form,user_id=user_id,book_id=book_id,book_name=book_name)
    
@app.route('/download',methods=['GET','POST'])
def download():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    #pdf_path = r'C:\Users\DAV\OneDrive\Desktop\mad1 project\static\Dummy(lib).pdf'
    if request.method == 'POST':
        book_id = request.form['book_id']
        price = request.form['price']
        # return send_file(pdf_path, as_attachment=True)
        return render_template('download.html',price=price)
    return render_template('Books.html')


@app.route('/get_pdf',methods=['GET','POST'])
def get_pdf():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    pdf_path = r'C:\Users\DAV\OneDrive\Desktop\mad1 project\static\Dummy(lib).pdf'
    if request.method == 'POST':
        return send_file(pdf_path, as_attachment=True)
    
@app.route('/admin',methods=['GET','POST'])
def index():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'admin':
        return redirect(url_for('login'))
    # Example query to get data for the graph
    data = db.session.query(UserRecord, Book).join(Book, UserRecord.book_id == Book.book_id).all()

    # Generate the graph
    graph_url = generate_graph(data)

    return render_template('admin_graph.html', graph_url=graph_url)

def generate_graph(data):
    # Count the occurrences of each book
    book_counts = Counter(book.name for entry, book in data)

    # Extract book names and their corresponding counts
    books = list(book_counts.keys())
    counts = list(book_counts.values())

    # Find the most issued book
    most_issued_book = max(book_counts, key=book_counts.get)

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(books, counts)
    plt.title('Most Issued Book')
    plt.xlabel('Book Name')
    plt.ylabel('Number of Issues')
    plt.xticks(rotation=45, ha='right')

    # Highlight the most issued book
    max_count = book_counts[most_issued_book]
    plt.bar(most_issued_book, max_count, color='red', label=f'Most Issued Book: {most_issued_book} ({max_count} times)')

    plt.legend()

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the plot image as base64
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f'data:image/png;base64,{graph_url}'

@app.route('/user_stats',methods=['GET','POST'])
def user_stats():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))

    book_info = db.session.query(issued_book.return_date, Book.name).join(Book, issued_book.book_id == Book.book_id).filter(issued_book.user_id == session.get('user')['user_id']).all()
    graph_url = generate_graphs(book_info)
    return render_template('user_graph.html', graph_url=graph_url)
def generate_graphs(book_info):
    due_dates = [datetime.strftime(book.return_date, '%Y-%m-%d') for book in book_info]
    due_dates_count = Counter(due_dates)
    sorted_due_dates = sorted(due_dates_count.keys())
    
# Extract x and y values for plotting
    x_values = sorted_due_dates
    y_values = [due_dates_count[date] for date in sorted_due_dates]

# Create the bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(x_values, y_values, color='skyblue')
    plt.title('Number of Books Currently Borrowed and Their Due Dates')
    plt.xlabel('Due Date')
    plt.ylabel('Number of Books')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Annotate the bars with the number of books
    for i, value in enumerate(y_values):
        plt.text(x_values[i], value + 0.1, str(value), ha='center')

    # # Show the plot
    # plt.show()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the plot image as base64
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f'data:image/png;base64,{graph_url}'




@app.route('/return_book',methods=['GET','POST'])
def return_book():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != 'customer':
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session.get('user')['user_id']
        book_id = request.form['book_id']
        return_date = datetime.now()
        issued = issued_book.query.filter_by(user_id=user_id,book_id=book_id).first()
        issued.return_date = return_date
        user_table = UserRecord.query.filter_by(user_id=user_id,book_id=book_id).first()
        user_table.return_date = return_date
        db.session.delete(issued)
        db.session.commit()
        return redirect(url_for('return_book'))
    
    return_info = db.session.query(issued_book,Book).join(Book,issued_book.book_id==Book.book_id).all()
    return render_template('return_books.html',returns=return_info)

