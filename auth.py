from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db
from .models import Book, AuthorNationality, Categories, Author, User, BookToCategory
import json

auth = Blueprint("auth", __name__)


@auth.route('/books', methods=['GET', 'POST'])
def books():
    all_books = Book.query.order_by(Book.title).distinct(Book.title)
    all_authors = Author.query
    book_to_cat = BookToCategory.query
    all_categories = Categories.query
    return render_template('books.html', books=all_books, authors=all_authors,
                           book_to_category=book_to_cat, categories=all_categories)


@auth.route('/book_add', methods=['GET', 'POST'])
def add_book():
    all_authors = Author.query.order_by(Author.first_name).all()
    all_categories = Categories.query.distinct(Categories.name)
    if request.method == 'POST':
        book = request.form.get('book')
        num_pages = request.form.get('pages')
        short_descrt = request.form.get('sh_descr')
        author_i = request.form.get('auth_id')
        book_category = request.form.get('category')
        release = request.form.get('release')
        new_book = Book(title=book, number_of_pages=num_pages,
                        short_description=short_descrt, author_id=author_i, release_date=release)
        book_to_category = BookToCategory(book_id=new_book.id, category_id=book_category)
        db.session.add(new_book)
        db.session.add(book_to_category)
        db.session.commit()
        flash('New book added', category='success')
        return redirect(url_for('auth.add_book'))
    return render_template('add_book.html', authors=all_authors, categories=all_categories)


@auth.route('/authors')
def authors():
    countries = AuthorNationality.query
    all_authors = Author.query.order_by(Author.first_name).all()
    return render_template('authors.html', authors=all_authors, nation=countries)


@auth.route('/authors_add', methods=['POST', 'GET'])
def add_author():
    countries = AuthorNationality.query.order_by(AuthorNationality.country).all()
    if request.method == 'POST':
        f_name = request.form.get('name')
        l_name = request.form.get('surname')
        nation_id = request.form.get('a_id')
        new_author = Author(first_name=f_name, last_name=l_name,  nationality_id=nation_id)
        db.session.add(new_author)
        db.session.commit()
        flash('You just added a new author', category='success')
        return redirect(url_for('auth.add_author'))
    return render_template('add_author.html', countries=countries)


@auth.route('/nations', methods=['POST', 'GET'])
def nations():
    if request.method == 'POST':
        nation = request.form.get('nations')
        new_country = AuthorNationality(country=nation)
        db.session.add(new_country)
        db.session.commit()
    countries = AuthorNationality.query.order_by(AuthorNationality.country).all()
    return render_template('nations.html', countries=countries)


@auth.route('/users', methods=['POST', 'GET'])
def users():
    all_users = User.query.order_by(User.first_name).all()
    today = datetime.now().year
    if request.method == 'POST':
        f_name = request.form.get('name')
        l_name = request.form.get('surname')
        b_date = request.form.get('birthdate')
        new_user = User(first_name=f_name, last_name=l_name, birth_date=b_date)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.users'))
    return render_template('users.html', users=all_users, now=today)


@auth.route('/category', methods=['POST', "GET"])
def category():
    if request.method == 'POST':
        get_category = request.form.get('category')
        new_category = Categories(name=get_category)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('auth.category'))

    categories = Categories.query.with_entities(Categories.name).distinct()
    return render_template('categories.html', categories=categories)


@auth.route('/review_add', methods=['POST', 'GET'])
def add_review():
    all_users = User.query.order_by(User.first_name).all()
    all_books = Book.query.order_by(Book.title).distinct(Book.title)
    return render_template('add_review.html', users=all_users, books=all_books)


@auth.route('/delete-book', methods=['POST'])
def delete_book():
    book = json.loads(request.data)
    bookId = book['bookId']
    mybook = Book.query.get(bookId)
    if mybook:
        db.session.delete(mybook)
        db.session.commit()
    return jsonify({})
