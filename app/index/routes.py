from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.models import User, Post, Tag, PostTag
from app.index import bp
from app.index.forms import RegistrationForm, LoginForm, PostForm, TagForm


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index/', methods=['GET', 'POST'])
@login_required
# def tag():
#     form = TagForm()
#     tag_name = Tag(name=form.name.data)
#     db.session.add(tag_name)
#     db.session.commit()
#     flash('Your tag has been added')
#     return render_template('index.html', title='Home', form=form)
def index(tag_1=None):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(heading=form.heading.data, body=form.body.data, author=current_user)
        tag_names = form.name.data.split(',')
        tags_post_obj = []

        print(tag_names)

        for tag_name in tag_names:

            print(type(tag_name))

            tag = Tag.query.filter_by(name=tag_name).first()

            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)

            post_tag = PostTag(post_id=post.id, tag_id=tag.id)

            tags_post_obj.append(post_tag)

        db.session.add_all(tags_post_obj)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added')
        return redirect(url_for('index.index'))
    return render_template('index.html', title='Home', form=form)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index.login'))

    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(fieldName, err)
    return render_template('register.html', title='Register', form=form)


# @bp.route('/user/<username>')
# @login_required
# def user_profile(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(user_id=user.id)
#     return render_template('user.html', user=user, posts=posts)


@bp.route('/index/add-tag/', methods=['GET', 'POST'])
@login_required
def tag_create():
    form = TagForm()
    tags_obj = []
    if form.validate_on_submit():
        tag_s = form.name.data.split(',')
        print(tag_s)
        for tag_s in tag_s:
            print(type(tag_s))
            tags_obj.append(Tag(name=tag_s))

        db.session.add_all(tags_obj)
        db.session.commit()
        return redirect(url_for('index.tag_create'))
    return render_template('addtag.html', title='Tags', form=form)


@bp.route('/index/all-tags/', methods=['GET', 'POST'])
@login_required
def tag_read():
    tags = Tag.query.order_by(Tag.timestamp.desc()).all()
    return render_template('tag.html', title='Tags', tags=tags)

# @bp.route('/index/test/', methods=['GET', 'POST'])
# @login_required
# def tag():
#     form = TagForm()
#     tag_name = Tag(name=form.name.data)
#     db.session.add(tag_name)
#     db.session.commit()
#     flash('Your tag has been added')
#     return render_template('test.html', title='Tag', form=form)
