from flask import render_template, url_for, redirect, request, flash
from app import app
from app.extensions import db
from app.form import LoginForm, CategoryForm, PostForm, RegisterForm
from app.model import Post, User
from flask_login import login_required, current_user, login_user, logout_user


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('/errors/404.html'), 404


@app.errorhandler(500)
def sever_error(e):
    return render_template('/errors/500.html'), 500


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return render_template('home.html')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if user.validate_password(password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('用户名或密码出错，请重新输入！')
                return render_template('login.html', form=form)
        else:
            return redirect(url_for('register'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/contact')
def contact():
    return render_template('contact.html')


def sidebar():
    post_all = Post.query.filter_by(user_id=current_user.id).all()
    vii = set()
    for post in post_all:
        vi = post.category
        vii.add(vi)
    categories = [x for x in vii]
    return categories


def sidebars():
    post_all = Post.query.all()
    vii = set()
    for post in post_all:
        vi = post.category
        vii.add(vi)
    categories = [x for x in vii]
    return categories


@app.route('/new_post', methods=['POST', 'GET'])
@login_required
def new_post():
    categories = sidebar()
    post_form = PostForm()
    category_form = CategoryForm()
    if post_form.validate_on_submit():
        title = post_form.title.data
        body = post_form.body.data
        category = category_form.category.data
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        current_user.post.append(post)
        db.session.commit()
        return redirect(url_for('post_list'))
    return render_template('new_post.html', post_form=post_form,
                           categories=categories, category_form=category_form)


@app.route('/show_post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    posts = Post.query.all()
    categories = sidebars()
    return render_template('show_post.html', categories=categories, post=post, posts=posts)


@app.route('/post_list')
def post_list():
    posts = Post.query.all()
    if posts is None:
        return render_template('post_list.html', posts=None, )
    categories = sidebars()
    page = request.args.get('page', type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=8)
    posts_pagination = pagination.items
    return render_template('post_list.html', categories=categories, pagination=pagination,
                           posts_pagination=posts_pagination)


@app.route('/my_post')
@login_required
def my_post():
    posts = current_user.post
    if posts is None:
        return render_template('post_list.html', posts=None, )
    categories = sidebar()
    page = request.args.get('page', type=int)
    pagination = Post.query.filter_by(
        user_id=current_user.id).order_by(
        Post.timestamp.desc()).paginate(page, per_page=8)
    posts_pagination = pagination.items
    return render_template(
            'post_list.html', categories=categories, pagination=pagination, posts_pagination=posts_pagination)


@app.route('/post_list_category/<string:category>')
def post_list_category(category):
    if current_user.is_authenticated:
        categories = sidebar()
        page = request.args.get('page', type=int)
        pagination = Post.query.filter_by(user_id=current_user.id).filter_by(category=category).paginate(page, per_page=8)
        posts_pagination = pagination.items
        return render_template('post_list.html', pagination=pagination,
                               categories=categories, posts_pagination=posts_pagination)
    categories = sidebars()
    page = request.args.get('page', type=int)
    pagination = Post.query.filter_by(category=category).paginate(page, per_page=8)
    posts_pagination = pagination.items
    return render_template('post_list.html', pagination=pagination,
                           categories=categories, posts_pagination=posts_pagination)


@app.route('/post_list_category/<int:user_id>')
def post_list_user(user_id):
    categories = sidebars()
    page = request.args.get('page', type=int)
    pagination = Post.query.filter_by(user_id=user_id).paginate(page, per_page=8)
    posts_pagination = pagination.items
    return render_template('post_list.html', pagination=pagination,
                           categories=categories, posts_pagination=posts_pagination)


@app.route('/delete_post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect_back()


@app.route('/edit_post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    post_form = PostForm()
    post = Post.query.get(post_id)
    posts = Post.query.all()
    categories = sidebars()
    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.body = post_form.body.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))
    post_form.title.data = post.title
    post_form.body.data = post.body
    return render_template('edit_post.html', post=post, categories=categories, posts=posts, post_form=post_form)
