from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Integer, ForeignKey, desc, asc
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from flask_gravatar import Gravatar
from forms import CreatePostForm, LoginForm, RegisterForm, CommentForm, User, BlogPost, db, Comment
from flask_migrate import Migrate
from faker import Faker as Fk
import smtplib
from smtplib import SMTP
from sqlalchemy import text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import dotenv

dotenv.load_dotenv()

# TODO
# skill-stacks.html: fix skill stack's collapse btn logic ✓
# clean-blog.min.css: mobile-friendly btn, navbar, font-size, margin setting ✓
# main.py: enable werkzeug.security hash password system
# sqldb: reset alembic_version


# make flask app
app = Flask(__name__)
# make secret key for wtf form (prevent CSRF attacks)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
print(os.environ.get("SECRET_KEY"))
ckeditor = CKEditor(app)
Bootstrap(app)
faker = Fk(['ko-KR', 'ja-JP'])



##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# with app.app_context():
#     db.create_all()


    
# instance of flask_login
login_manager = LoginManager()
# bind flask app with LoginManager()
login_manager.init_app(app)

# with app.app_context():
#     db.session.query(User).delete()


# login_manager, load_user setting for login_manager to pass the user id from db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=["POST", "GET"])
def home():
    masthead_text = 'HOME'
    subheading_text = 'Welcome to JiwooHub!'
    return render_template('index.html',
                           masthead_text=masthead_text,
                           subheading_text=subheading_text)


@app.route('/introduction', methods=["POST", "GET"])
def introduction():
    masthead_text = 'INTRODUCTION'
    subheading_text = 'About Jiwoo Kim'
    # check flask_login status with UserMixin conditions (returns false if not met)
    if current_user.is_authenticated:
        print(f"admin_auth: {current_user.is_admin}")
        print('currently logged in')
        print(current_user.name)

    else:
        print('unlogged-in')
    posts = BlogPost.query.all()
    return render_template("introduction.html",
                           all_posts=posts,
                           masthead_text=masthead_text,
                           subheading_text=subheading_text)


@app.route('/gen-post', methods=["POST", "GET"])
def gen_post():
    masthead_text = None
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

    return render_template('portfolio.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    masthead_text = 'REGISTER'
    subheading_text = 'Sign up to JiwooHub'
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
                    password=generate_password_hash(form.password.data),
                    is_admin=True
                )
            else:
                to_add = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data)
                )
            db.session.add(to_add)
            db.session.commit()
            flash('Registered Successfully!')
            return redirect('/login')
    return render_template("register.html",
                           form=form,
                           error=error,
                           masthead_text=masthead_text, subheading_text=subheading_text)


@app.route('/login', methods=['POST', 'GET'])
def login():
    masthead_text = 'LOGIN'
    subheading_text = 'Login to JiwooHub'
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        # find form matching user in db
        user_db = db.session.query(User).filter_by(email=form.email.data).first()
        if user_db is not None:
            print(user_db.password)
            print(form.password.data)
            if check_password_hash(user_db.password, form.password.data):
                # login with the sql db of the form matching user
                login_user(user_db)
                return redirect(url_for('home'))
        else:
            error = "Account Doesn't Exists"
    return render_template("login.html", form=form, error=error, masthead_text=masthead_text,
                           subheading_text=subheading_text)


@app.route('/logout')
def logout():
    # change current_user's status to logout
    logout_user()
    return redirect(url_for('home'))


@app.route('/portfolio')
def portfolio():
    posts = BlogPost.query.order_by(asc(BlogPost.date)).all()
    masthead_text = "PORTFOLIO"
    subheading_text = "See My Works"
    # check flask_login status with UserMixin conditions (returns false if not met)
    if current_user.is_authenticated:
        print(f"admin_auth: {current_user.is_admin}")
        print('currently logged in')
        print(current_user.name)

    else:
        print('unlogged-in')
    posts = BlogPost.query.all()
    return render_template("portfolio.html", all_posts=posts, masthead_text=masthead_text,
                           subheading_text=subheading_text)


@app.route("/post/<int:post_id>", methods=["GET"])
def show_post(post_id):
    masthead_text = 'PORTFOLIO'
    subheading_text = 'See the Works'
    editor_auth = False
    # show comments
    blogpost_instance = BlogPost.query.get(post_id)
    print(blogpost_instance)
    comments = Comment.query.filter_by(blogpost_id=post_id).all()
    # remove comments
    if blogpost_instance and blogpost_instance.user:
        user_name = blogpost_instance.user.name
        comments = Comment.query.filter_by(blogpost_id=post_id).all()
        # remove comments
        try:
            if current_user.is_authenticated:
                if blogpost_instance.user.name == current_user.name:
                    editor_auth = True
        except AttributeError:
            pass
    return render_template("post.html",
                           comments=comments,
                           comment_form=CommentForm(),
                           post=blogpost_instance,
                           name='Jiwoo',
                           editor_auth=editor_auth,
                           masthead_text=masthead_text,
                           subheading_text=subheading_text)


@app.route("/skill-stacks")
def about():
    masthead_text = "Skill Stack"
    subheading_text = 'My Developer Skills'
    return render_template("skill-stacks.html", masthead_text=masthead_text, subheading_text=subheading_text)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    masthead_text = 'CONTACT'
    subheading_text = 'Contact Jiwoo'
    return render_template("contact.html", masthead_text=masthead_text, subheading_text=subheading_text)


@app.route('/submit', methods=['POST'])
def submit():
    MY_EMAIL = os.environ.get('MY_EMAIL')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        message = request.form.get('message', '')
        # send contact info to my email
        msg = MIMEMultipart()
        msg['From'] = 'JiwooHub'
        msg['To'] = MY_EMAIL
        msg['Subject'] = 'New Contact Info Submission'
        body = f"name: {name}\nemail: {email}\nphone: {phone}\nmessage: {message}"
        msg.attach(MIMEText(body, 'plain'))

        try:
            with SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
                print('login successful')
                connection.send_message(msg)
                print("Email Sent Successfully")
        except smtplib.SMTPException as e:
            print(f"Error: {e}")
        return redirect(url_for('contact'))


@app.route("/post_1")
def post_1():
    post = BlogPost.query.get(1)
    comment_form = CommentForm()
    return render_template('post_1.html', post=post, comment_form=comment_form)


@app.route("/make-post", methods=["POST", "GET"])
@login_required
def add_new_post():
    masthead_text = 'MAKE POST'
    subheading_text = 'Add to Portfolio'
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            date=date.today().strftime("%B %d, %Y")
        )
        print(date.today().strftime("%B %d, %Y"))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("portfolio"))
    return render_template("make-post.html", form=form,
                           masthead_text=masthead_text, subheading_text=subheading_text)


@app.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
@login_required
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
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
    if not current_user.is_admin:
        flash('Access denied: You must be an admin to access this page.', 'danger')
        return redirect(url_for('home'))
    comments_to_delete = Comment.query.filter_by(blogpost_id=post_id)
    for comment in comments_to_delete:
        db.session.delete(comment)
        db.session.commit()
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('portfolio'))


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


@app.route('/bugfix', methods=['POST', 'GET'])
def bugfix():
    return render_template('bugfix.html')


if __name__ == "__main__":
    app.run(debug=True, port=3240)
