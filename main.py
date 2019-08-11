# [START gae_python37_cloudsql_mysql]
import os

from flask import Flask, render_template, url_for, redirect, flash
from forms import SignUpForm, LoginForm, SlotDateSearchForm, ZipSearchForm, VenueDateForm
import pymysql
from func.mainfunctions import MainFunctions


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
app.config['SECRET_KEY'] = '294d86e9fd5e4b179261796459238269'
userid=0

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/home")
def home():
    return render_template("home.html")
    

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        func = MainFunctions()
        userdata = {}
        userdetail = {}
        userdata['username'] = form.username.data
        userdata['password'] = form.password.data


        result = func.log_in(userdata)
        if result[0]==1:
                # request.session['username_sh']=userdata['username']
                # request.session['adminuser']=result[1]
                # request.session['userstatus']=result[2]
                print(result[1], result[2])
                if result[2]!='I':
                    userid=result[3]
                    if result[1]=='A':
                        userdetail['admin']=True
                    else:
                        userdetail['admin']=False
                else:
                    return "<h2 align='center'>Sorry, your account is in an Inactive state.<br> Please contact administrator to activate it.</h2><br><a href='home'>Home</a>"
                return redirect(url_for('home'))
        else:
            return ("<h2>Invalid username or password.</h2>")

    return render_template("user_login.html", title="login", form=form)


@app.route("/signup", methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        func = MainFunctions()
        userdata = {}
        userdata['username'] = form.username.data
        userdata['firstname'] = form.firstname.data
        userdata['lastname'] = form.lastname.data
        userdata['email'] = form.email.data
        userdata['password'] = form.password.data
        userdata['zipcode'] = form.zipcode.data
        userdata['isadmin'] = "N"
        func.add_user(userdata)
        flash(f'{form.firstname.data}, your account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template("user_signup.html", title="Sign Up", form=form)


# Display venues for Zip Code
@app.route("/zipsearch", methods=['GET','POST'])
def zipsearch():
    form = ZipSearchForm()
    if form.validate_on_submit():
        func = MainFunctions()
        venuelist = func.get_venues_for_zipcode(form.zipcode.data)
        print(venuelist)
        return render_template('display_venues.html', list=venuelist)
    return render_template("zip_search.html", title="SearchZip", form=form)


@app.route("/venues", methods=['GET','POST'])
def venues():
    if form.validate_on_submit():
        func = MainFunctions()
        venuelist = func.get_venues_for_zipcode(form.zipcode.data)
        return redirect(url_for('venues'))
    return render_template("zip_search.html", title="Venues")


@app.route("/venueevents", methods=['GET','POST'])
def venueevents(venue):
    func = MainFunctions()
    eventlist = func.display_events_for_venue_id(venueid)
    return render_template("venue_events.html", title="VenueEvents", list=eventlist)


@app.route("/joinevent", methods=['GET','POST'])
def joinevent(eventid):
    func = MainFunctions()
    func.user_joins_event(userid,eventid)
    return render_template("venue_events.html", title="VenueEvents", list=eventlist)



@app.route('/now')
def main():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='root', password='root1234', host=host, db='soccerhoursdb')

    with cnx.cursor() as cursor:
        cursor.execute('SELECT NOW() as now;')
        result = cursor.fetchall()
        current_time = result[0][0]
    cnx.close()

    return str(current_time)




if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080,debug=True)



