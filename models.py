from . import db


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id", ondelete="cascade"))
    number_of_pages = db.Column(db.Integer)
    short_description = db.Column(db.String)
    rating = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)
    categories = db.relationship('BookToCategory', cascade='all, delete, delete-orphan')


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    birth_date = db.Column(db.DateTime)


class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    feedback = db.Column(db.Integer)


class BookLog(db.Model):
    __tablename__ = 'booklog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    nationality_id = db.Column(db.Integer, db.ForeignKey("author_nationality.id"))


class AuthorNationality(db.Model):
    __tablename__ = 'author_nationality'

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String)


class BookToCategory(db.Model):
    __tablename__ = 'book_to_category'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete='CASCADE'))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id", ondelete='CASCADE'))


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
