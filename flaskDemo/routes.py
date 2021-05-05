import os
import secrets
import datetime
import mysql.connector
from mysql.connector import Error
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, TestDateForm
from flaskDemo.models import Test, Testing_Site, Users, Vaccination, Vaccination_Site, Vaccine, connect
from flask_login import login_user, current_user, logout_user, login_required

times = ['0700', '0715', '0730', '0745', '0800', '0815', '0830', '0845', '0900', '0915', '0930', '0945', '1000', '1015', '1030',
         '1045', '1100', '1115', '1130', '1145', '1200', '1215', '1230', '1245', '1300', '1315', '1330', '1345', '1400', '1415',
         '1430', '1445', '1500', '1515', '1530', '1545', '1600', '1615', '1630', '1645', '1700', '1715', '1730', '1745', '1800', '1815', '1830', '1845']


@app.route("/")
@app.route("/home")
def home():
    #posts = Post.query.all()
    #return render_template('home.html', posts=posts)
    return render_template('home.html')


##@app.route("/about")
##def about():
##    return render_template('about.html', title='About')


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
        flash('Your account has been created! You are now able to log in.', 'success')
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

##@app.route("/testing", methods=['GET', 'POST'])
##@login_required
##def testing():
##    return render_template('testing.html', title= 'Testing History')
##  #  testHist = Testing_Site.query.all()
##
##   # query = Testing_Site.query.join(Test, Testing_Site.testID == Test.testID) \
##    #        .add_columns(Testing_Site.testAddress, Testing_Site.testCity, Testing_Site.testZip, Test.testResult) \
##     #       .group_by(Testing_Site.testID)
##    testHist = Test.query.all()
##
##    query = Test.query.join(Testing_Site, Test.testID == Testing_Site.testID) \
##           .add_columns(Test.id, Testing_Site.testAddress, Testing_Site.testCity, Testing_Site.testZip, Test.testResult) \
##
##    return render_template('testing.html', title= 'Testing History', testHist = query)
##
##@app.route("/vaccine", methods=['GET', 'POST'])
##@login_required
##def vaccine():
##    vachist = Vaccination.query.all()
##    
##    quer= Vaccination.query.join( Vaccine, Vaccination.vaccineBrand== Vaccine.vaccineBrand ) \
##    .add_columns(Vaccine.vaccineDistDate, Vaccination.id, Vaccination.vaccineBrand) \
##    .group_by(Vaccination.vaccineLotNum)
##  
##    return render_template('vaccine.html', title= 'Vaccine History', vachist= quer)

@app.route("/testing", methods=['GET'])
@login_required
def testing():
    conn = mysql.connector.connect(host='localhost',
                                               database='covid',
                                               user='student',
                                               password='student')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM test t INNER JOIN testing_site ts ON t.testID=ts.testID WHERE t.id = " + str(current_user.id) + " ORDER BY t.testDate DESC")
    testing = cursor.fetchall()
    cursor.close()
    return render_template('test_history.html', posts=testing, datetime=datetime.date.today())

@app.route("/testing/delete/<string:test_date>/<int:test_ID>", methods=['GET'])
@login_required
def testing_delete(test_date, test_ID):
    test = Test.query.filter_by(id=current_user.id, testID=test_ID, testDate=test_date).first()
    if test.id != current_user.id:
        abort(403)
    db.session.delete(test)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('testing'))

@app.route("/vaccine", methods=['GET'])
@login_required
def vaccine():
    conn = mysql.connector.connect(host='localhost',
                                               database='covid',
                                               user='student',
                                               password='student')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vaccination v INNER JOIN vaccine vx ON v.vaccineBrand = vx.vaccineBrand AND v.vaccineLotNum = vx.vaccineLotNum INNER JOIN vaccination_site vs ON vx.vaxID=vs.vaxID WHERE v.id = " + str(current_user.id) + " ORDER BY vx.vaccineDistDate DESC")
    vaccine = cursor.fetchall()
    cursor.close()
    return render_template('vaccine_history.html', posts=vaccine, datetime=datetime.date.today())

##@app.route("/vaccine/delete/<string:vaccine_brand>/<string:vaccine_num>", methods=['GET'])
##@login_required
##def vaccine_delete(vaccine_brand, vaccine_num):
##    vaccine = Vaccination.query.filter_by(id=current_user.id, vaccineBrand=vaccine_brand, vaccineLotNum=vaccine_num).first()
##    if vaccine.id != current_user.id:
##        abort(403)
##    db.session.delete(vaccine)
##    db.session.commit()
##    flash('Your post has been deleted!', 'success')
##    return redirect(url_for('home'))
  

@app.route("/covid_test_appointment", methods=['GET'])
@login_required
def covid_test_appointment():
    testing_site = Testing_Site.query.all()
    return render_template('covid_test_appointment.html', posts=testing_site)

@app.route("/covid_test_appointment/<int:test_site_id>", methods=['GET', 'POST'])
@login_required
def covid_test_appointment_site(test_site_id):
    form = TestDateForm()
    testing_site = Testing_Site.query.filter_by(testID=test_site_id)
    testing_site_first = testing_site.first()
    if form.validate_on_submit():
        if (form.testDate.data.weekday() == 0 and testing_site_first.testMonday==0) or (form.testDate.data.weekday() == 1 and testing_site_first.testTuesday==0) \
        or (form.testDate.data.weekday() == 2 and testing_site_first.testWednesday==0) \
        or (form.testDate.data.weekday() == 3 and testing_site_first.testThursday==0) or (form.testDate.data.weekday() == 4 and testing_site_first.testFriday==0) \
        or (form.testDate.data.weekday() == 5 and testing_site_first.testSaturday==0) or (form.testDate.data.weekday() == 6 and testing_site_first.testSunday==0):
            flash('This testing site is not open on that day. Please try again.', 'danger')
            return redirect(url_for('covid_test_appointment_site', test_site_id=test_site_id))
        return redirect(url_for('covid_test_appointment_site_date', test_site_id=test_site_id, test_date=str(form.testDate.data)))              
    return render_template('covid_test_appointment2.html', posts=testing_site, form=form)

@app.route("/covid_test_appointment/<int:test_site_id>/<string:test_date>", methods=['GET'])
@login_required
def covid_test_appointment_site_date(test_site_id, test_date):
    testing_site = Testing_Site.query.filter_by(testID=test_site_id)
    local_times = times.copy()
    local_times_remove = []

    for time in local_times:
        #Remove times from time array where there is an existing appointment already.
        conn = mysql.connector.connect(host='localhost',
                                               database='covid',
                                               user='student',
                                               password='student')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM test WHERE testID = " + str(test_site_id) + " AND testTime = " + time + " AND testDate = CAST(" + test_date + " AS DATE)")
        time_found = cursor.fetchone()
        if time_found is not None:
            local_times_remove.append(time)
            cursor.close
            continue

        cursor.close

        conn = mysql.connector.connect(host='localhost',
                                               database='covid',
                                               user='student',
                                               password='student')
        cursor = conn.cursor(dictionary=True)
        #Remove times from time array where selected testing site not open.
        cursor.execute("SELECT * FROM testing_site WHERE testID = " + str(test_site_id) + " AND (CAST(testOpen AS TIME) >= CAST(" + str(time) + " AS TIME) OR CAST(testClose AS TIME) <= CAST(" + str(time) + " AS TIME))")
        time_found = cursor.fetchone()
        if time_found is not None:
            local_times_remove.append(time)
            cursor.close
            continue

    for time in local_times_remove:
        local_times.remove(time)
    
    cursor.close
    return render_template('covid_test_appointment3.html', posts=testing_site, test_date=test_date, times=local_times)
    #return render_template('covid_test_appointment2.html', posts=testing_site)

@app.route("/covid_test_appointment/<int:test_site_id>/<string:test_date>/<string:test_time>", methods=['GET'])
@login_required
def covid_test_appointment_site_date_time(test_site_id, test_date, test_time):
    testing_site = Testing_Site.query.filter_by(testID=test_site_id)
    return render_template('covid_test_appointment4.html', posts=testing_site, test_date=test_date, test_time=test_time)

@app.route("/covid_test_appointment/<int:test_site_id>/<string:test_date>/<string:test_time>/confirmed", methods=['GET', 'POST'])
@login_required
def covid_test_appointment_site_date_time_confirmed(test_site_id, test_date, test_time):
    test = Test(id=current_user.id, testID=test_site_id, testDate=test_date, testTime=test_time, testResult="")
    db.session.add(test)
    db.session.commit()
    flash('Your testing appointment has been scheduled!', 'success')
    return redirect(url_for('home'))

#Vaccine Appointment Below:
@app.route("/vaccination_appointment", methods=['GET'])
@login_required
def vaccination_appointment():
    user_vaccines = Vaccination.query.filter_by(id=current_user.id).all()
    i = 0
    if user_vaccines is not None:
        for row in user_vaccines:
            i += 1
        if i >= 2:
            flash('You have already received 2 doses of the COVID vaccine', 'danger')
            return redirect(url_for('home'))
        elif i == 1:
            user_vaccines_first = Vaccination.query.filter_by(id=current_user.id).first()
##            user_vaccine_first_brand = str(user_vaccines_first.vaccineBrand)
##            print(user_vaccine_first_brand)
##            cursor.execute("SELECT v.vaccineBrand, v.vaccineLotNum, v.vaccineDistDate, vs.vaxName, vs.vaxAddress, vs.vaxZip, vs.vaxCity, vs.vaxOpen, vs.vaxClose, vs.vaxSunday, vs.vaxMonday, vs.vaxTuesday, vs.vaxWednesday " +\
##                           "vs.vaxThursday, vs.vaxFriday, vs.vaxSaturday FROM vaccine v INNER JOIN vaccine_site vs ON v.vaxID=vs.vaxID WHERE v.vaccineBrand = " + user_vaccines_first.vaccineBrand + " ORDER BY v.vaccineDistDate ASC")
            conn = mysql.connector.connect(host='localhost',
                                               database='covid',
                                               user='student',
                                               password='student')
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vaccine v INNER JOIN vaccination_site vs ON v.vaxID=vs.vaxID WHERE v.vaccineBrand = '" + str(user_vaccines_first.vaccineBrand) + "' ORDER BY v.vaccineDistDate ASC")
            vaccine = cursor.fetchall()
            cursor.close()
            return render_template('vaccination_appointment.html', posts=vaccine)

    conn = mysql.connector.connect(host='localhost',
                                               database='covid',
                                               user='student',
                                               password='student')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vaccine v INNER JOIN vaccination_site vs ON v.vaxID=vs.vaxID ORDER BY v.vaccineDistDate ASC")
    vaccine = cursor.fetchall()
    cursor.close()
    return render_template('vaccination_appointment.html', posts=vaccine)

##@app.route("/vaccination_appointment/<int:vax_site_id>/<string:vaccine_num>", methods=['GET', 'POST'])
##@login_required
##def vaccination_appointment_site(vax_site_id, vaccine_num):
##    form = TestDateForm()
##    testing_site = Testing_Site.query.filter_by(vaxID=vax_site_id)
##    testing_site_first = testing_site.first()
##    if form.validate_on_submit():
##        if (form.testDate.data.weekday() == 0 and testing_site_first.testMonday==0) or (form.testDate.data.weekday() == 1 and testing_site_first.testTuesday==0) \
##        or (form.testDate.data.weekday() == 2 and testing_site_first.testWednesday==0) \
##        or (form.testDate.data.weekday() == 3 and testing_site_first.testThursday==0) or (form.testDate.data.weekday() == 4 and testing_site_first.testFriday==0) \
##        or (form.testDate.data.weekday() == 5 and testing_site_first.testSaturday==0) or (form.testDate.data.weekday() == 6 and testing_site_first.testSunday==0):
##            flash('This testing site is not open on that day. Please try again.', 'danger')
##            return redirect(url_for('covid_test_appointment_site', test_site_id=test_site_id))
##        return redirect(url_for('covid_test_appointment_site_date', posts=testing_site, test_site_id=test_site_id, test_date=str(form.testDate.data)))              
##    return render_template('covid_test_appointment2.html', posts=testing_site, form=form)

@app.route("/vaccination_appointment/<int:vax_site_id>/<string:vaccine_brand>/<string:vaccine_num>", methods=['GET'])
@login_required
def vaccination_appointment_site_num(vax_site_id, vaccine_brand, vaccine_num):
    vaccination_site = Vaccination_Site.query.filter_by(vaxID=vax_site_id)
    vaccine = Vaccine.query.filter_by(vaccineBrand=vaccine_brand, vaccineLotNum=vaccine_num)
    local_times = times.copy()
    local_times_remove = []

    for time in local_times:
        #Remove times from time array where there is an existing appointment already.
        conn = mysql.connector.connect(host='localhost',
                                               database='covid',
                                               user='student',
                                               password='student')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vaccination v1 INNER JOIN vaccine v2 ON v1.vaccineBrand=v2.vaccineBrand AND v1.vaccineLotNum = v2.vaccineLotNum WHERE v1.vaccineBrand = '" \
                       + vaccine_brand + "' AND v1.vaccineTime = " + time)
        time_found = cursor.fetchone()
        if time_found is not None:
            local_times_remove.append(time)
            cursor.close
            continue

        cursor.close
        conn = mysql.connector.connect(host='localhost',
                                               database='covid',
                                               user='student',
                                               password='student')
        cursor = conn.cursor(dictionary=True)
        #Remove times from time array where selected testing site not open.
        cursor.execute("SELECT * FROM vaccination_site WHERE vaxID = " + str(vax_site_id) + " AND (CAST(vaxOpen AS TIME) >= CAST(" + str(time) + " AS TIME) OR CAST(vaxClose AS TIME) <= CAST(" + str(time) + " AS TIME))")
        time_found = cursor.fetchone()
        if time_found is not None:
            local_times_remove.append(time)
            cursor.close
            continue

    for time in local_times_remove:
        local_times.remove(time)
    
    cursor.close
    return render_template('vaccination_appointment3.html', posts=vaccination_site, vaccine=vaccine, times=local_times)
    #return render_template('covid_test_appointment2.html', posts=testing_site)

@app.route("/vaccination_appointment/<int:vax_site_id>/<string:vaccine_brand>/<string:vaccine_num>/<string:vaccine_time>", methods=['GET'])
@login_required
def vaccination_appointment_site_num_time(vax_site_id, vaccine_brand, vaccine_num, vaccine_time):
    vaccination_site = Vaccination_Site.query.filter_by(vaxID=vax_site_id)
    vaccine = Vaccine.query.filter_by(vaccineBrand=vaccine_brand, vaccineLotNum=vaccine_num)
    return render_template('vaccination_appointment4.html', posts=vaccination_site, vaccine=vaccine, vaccine_time=vaccine_time)

@app.route("/vaccination_appointment/<int:vax_site_id>/<string:vaccine_brand>/<string:vaccine_num>/<string:vaccine_time>/confirmed", methods=['GET', 'POST'])
@login_required
def vaccination_appointment_site_num_time_confirmed(vax_site_id, vaccine_brand, vaccine_num, vaccine_time):
    vaccination = Vaccination(id=current_user.id, vaccineBrand=vaccine_brand, vaccineLotNum=vaccine_num, vaccineTime=vaccine_time)
    db.session.add(vaccination)
    db.session.commit()
    flash('Your vaccination appointment has been scheduled!', 'success')
    return redirect(url_for('home'))


##@app.route("/schedule", methods=['GET', 'POST'])
##@login_required
##def schedule():
##    
##    form= PostForm()
##    if form.validate_on_submit():
##     
##        db.session.commit()
##    
##    return render_template('schedule.html', title= 'Schedule Vaccine', form=form) 
  

##@app.route("/post/new", methods=['GET', 'POST'])
##@login_required
##def new_post():
##    form = PostForm()
##    if form.validate_on_submit():
##        post = Post(title=form.title.data, content=form.content.data, author=current_user)
##        db.session.add(post)
##        db.session.commit()
##        flash('Your post has been created!', 'success')
##        return redirect(url_for('home'))
##    return render_template('create_post.html', title='New Post',
##                           form=form, legend='New Post')
##
##
##@app.route("/post/<int:post_id>")
##def post(post_id):
##    post = Post.query.get_or_404(post_id)
##    return render_template('post.html', title=post.title, post=post)
##
##
##@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
##@login_required
##def update_post(post_id):
##    post = Post.query.get_or_404(post_id)
##    if post.author != current_user:
##        abort(403)
##    form = PostForm()
##    if form.validate_on_submit():
##        post.title = form.title.data
##        post.content = form.content.data
##        db.session.commit()
##        flash('Your post has been updated!', 'success')
##        return redirect(url_for('post', post_id=post.id))
##    elif request.method == 'GET':
##        form.title.data = post.title
##        form.content.data = post.content
##    return render_template('create_post.html', title='Update Post',
##                           form=form, legend='Update Post')
##
##
##@app.route("/post/<int:post_id>/delete", methods=['POST'])
##@login_required
##def delete_post(post_id):
##    post = Post.query.get_or_404(post_id)
##    if post.author != current_user:
##        abort(403)
##    db.session.delete(post)
##    db.session.commit()
##    flash('Your post has been deleted!', 'success')
##    return redirect(url_for('home'))
