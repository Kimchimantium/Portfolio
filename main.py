from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from flask_gravatar import Gravatar
from forms import CreatePostForm, LoginForm, RegisterForm, CommentForm, User, BlogPost, db, Comment
from flask_migrate import Migrate
from faker import Faker as Fk
import os

from dotenv import load_dotenv
load_dotenv()


# make flask app
app = Flask(__name__)
# make secret key for wtf form (prevent CSRF attacks)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
secret_key = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)
faker = Fk(['ko-KR', 'ja-JP'])

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()

# instance of flask_login
login_manager = LoginManager()
# bind flask app with LoginManager()
login_manager.init_app(app)


# login_manager, load_user setting for login_manager to pass the user id from db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=["POST", "GET"])
def get_all_posts():
    # check flask_login status with UserMixin conditions (returns false if not met)
    if current_user.is_authenticated:
        print(f"admin_auth: {current_user.is_admin}")
        print('currently logged in')
        print(current_user.name)
    else:
        print('unlogged-in')
    posts=BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/gen-post', methods=["POST", "GET"])
def gen_post():
    print(current_user.name)
    post_user = User(
        name=current_user.name,
        email=faker.email(),
        password="asdf1319"
    )
    new_post = BlogPost(
        user=post_user,
        title=faker.sentence(),
        subtitle=faker.sentence(),
        date=faker.date(),
        body=faker.paragraph(100),
        img_url='https://picsum.photos/640/480'
    )
    if new_post:
        print(new_post.user)
        db.session.add(new_post)
        db.session.commit()

    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_2.data:
            error = 'Check Password Again'
        elif User.query.filter_by(email=form.email.data).first() is not None:
            error = 'Account Already Exists'
        else:
            if form.email.data == os.environ.get('ADMIN_EMAIL'):
                to_add = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=form.password.data,
                    is_admin = True
                )
            else:
                to_add = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=form.password.data
                )
            db.session.add(to_add)
            db.session.commit()
            flash('Registered Successfully!')
            return redirect('/login')
    return render_template("register.html",
                           form=form,
                           error=error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        # find form matching user in db
        user_db = db.session.query(User).filter_by(email=form.email.data).first()
        if user_db is not None:
            print(user_db.password)
            print(form.password.data)
            if user_db.password == form.password.data:
                # login with the sql db of the form matching user
                login_user(user_db)
                return redirect('/')
        else:
            error = "Account Doesn't Exists"
    return render_template("login.html", form=form, error=error)


@app.route('/logout')
def logout():
    # change current_user's status to logout
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_post(post_id):
    editor_auth = False
    # show comments
    blogpost_instance = BlogPost.query.get(post_id)
    comments = Comment.query.filter_by(blogpost_id=post_id).all()
    # remove comments
    if current_user.is_authenticated:
        if blogpost_instance.user.name == current_user.name:
            editor_auth = True
    return render_template("post.html",
                           comments=comments,
                           comment_form=CommentForm(),
                           post=blogpost_instance,
                           name=blogpost_instance.user.name,
                           editor_auth=editor_auth)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=["POST", "GET"])
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user.name,
            date=date.today().strftime("%B %d, %Y")
        )
        print(date.today().strftime("%B %d, %Y"))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
@login_required
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    print(post.user.name)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    comments_to_delete = Comment.query.filter_by(blogpost_id=post_id)
    for comment in comments_to_delete:
        db.session.delete(comment)
        db.session.commit()
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/comment/<int:post_id>", methods=["POST", "GET"])
def comment(post_id):
    post_to_comment = BlogPost.query.get(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment(
            blogpost=post_to_comment,
            text=form.comment.data
        )
        db.session.add(new_comment)
        db.session.commit()
    comment_added = Comment.query.get(post_id)
    return redirect(url_for("show_post", post_id=post_id))

@app.route('/delete_comment/<int:post_id>', methods={"POST", "GET"})
def delete_comment(post_id):
    text = request.args.get('text')
    to_delete = Comment.query.filter_by(text=text).first()
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for('show_post', post_id=post_id))


if __name__ == "__main__":
    app.run(debug=True, port=9080)

