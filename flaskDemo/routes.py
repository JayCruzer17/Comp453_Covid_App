import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskDemo.models import User, Post, Test, Testing_Site, Users, Vaccination, Vaccination_Site, Vaccine
from flask_login import login_user, current_user, logout_user, login_required




@app.route("/")
@app.route("/home")
def home():
    #posts = Post.query.all()
    #return render_template('home.html', posts=posts)
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user = Users(username=form.username.data, firstName=form.firstName.data, lastName=form.lastName.data, password=form.password.data, birthDate=form.birthDate.data, userAddress=form.address.data,
                     userZip=form.zipcode.data, userCity=form.city.data, email=form.email.data, gender=form.gender.data, userPhone=form.phone.data, insuranceProvider=form.insurancePro.data, insuranceNum=form.insuranceNum.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        #return render_template('register.html', title='Register', form=form)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


##def save_picture(form_picture):
##    random_hex = secrets.token_hex(8)
##    _, f_ext = os.path.splitext(form_picture.filename)
##    picture_fn = random_hex + f_ext
##    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
##
##    output_size = (125, 125)
##    i = Image.open(form_picture)
##    i.thumbnail(output_size)
##    i.save(picture_path)
##
##    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        #if form.picture.data:
            #picture_file = save_picture(form.picture.data)
            #current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.userPhone = form.phone.data
        current_user.userAddress = form.address.data
        current_user.userZip = form.zipcode.data
        current_user.userCity = form.city.data
        current_user.insuranceProvider = form.insurancePro.data
        current_user.insuranceNum = form.insuranceNum.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.userPhone
        form.address.data = current_user.userAddress
        form.zipcode.data = current_user.userZip
        form.city.data = current_user.userCity
        form.insurancePro.data = current_user.insuranceProvider
        form.insuranceNum.data = current_user.insuranceNum
        return render_template('account.html', title='Account', form=form)
    #image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
##    return render_template('account.html', title='Account',
##                           image_file=image_file, form=form)


@app.route("/schedule", methods=['GET', 'POST'])
@login_required
def schedule():
    
    form= PostForm()
    if form.validate_on_submit():
     
        db.session.commit()
    
    return render_template('schedule.html', title= 'Schedule Vaccine', form=form) 
  

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
