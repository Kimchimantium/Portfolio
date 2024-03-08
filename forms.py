from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

db = SQLAlchemy()


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField(label="Blog Image URL")
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class CommentForm(FlaskForm):
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment", render_kw={'class': 'btn btn-primary btn-sm'})


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired()])
    password = PasswordField(label='Password')
    submit = SubmitField(label="Submit")


class RegisterForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired()])
    password = PasswordField(label='Password')
    password_2 = PasswordField(label='*Password')
    submit = SubmitField(label='Submit')


class User(UserMixin, db.Model):
    # UserMixin attributes
    def is_active(self):
        return True
    # db.Model attributes
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False, unique=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    blogposts = relationship("BlogPost", back_populates="user")


class BlogPost(db.Model):
    """ by setting 'class BlogPost(db.Model)' db makes a table called 'blogpost' with the fields
    in the class which are id, author, title ...etc"""
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user_info.id"))
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=True)
    user = relationship("User", back_populates='blogposts')
    comments = relationship("Comment", back_populates="blogpost")


class Comment(db.Model):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    text = Column(db.String(300), nullable=False)
    blogpost_id = Column(Integer, ForeignKey('blog_posts.id'))
    blogpost = relationship("BlogPost", back_populates="comments")

class TodoUser(UserMixin, db.Model):
    __tablename__ = 'todo_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(512), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    description = db.Column(db.String(200))
    importance = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('todo_user.id'))
