# [START gae_python37_cloudsql_mysql]
import os

from flask import Flask, render_template, url_for, redirect, flash, jsonify, request, session
from forms import SignUpForm, LoginForm, SlotDateSearchForm, ZipSearchForm, VenueDateForm, StartEventForm
import pymysql
from func.mainfunctions import MainFunctions
from func.commonfunctions import CommonFunctions


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
app.config['SECRET_KEY'] = '294d86e9fd5e4b179261796459238269'
userid=0
venueid=0
eventid=0

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/home")
def home():
    return render_template("home.html", admin=session['admin'])

@app.route("/admin")
def admin():
    if 'admin' in session:
        if session['admin'] == 'A':
            return render_template("admin.html")
        else:
            return "<h2>Sorry, you are not an admin user at Soccer Hours</h2>"
    else:
        return render_template('user_login.html', title='Login')

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
                    session['userid']=result[3]
                    session['admin']=result[1]
                    session['username']=result[4]
                    print("Logged in : "+result[4])
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
        # return redirect(url_for('venues', list=venuelist))
        return render_template('display_venues.html', list=venuelist)
    return render_template("zip_search.html", title="SearchZip", form=form)

# Start an Event
@app.route("/startevent", methods=['GET','POST'])
def startevent():
    form = StartEventForm()
    func = CommonFunctions()
    venuelist = func.get_all_venues()
    print("Startevent Body")
    if form.validate_on_submit():
        print("submitted")
        print(session['username'])
        mainfunc = MainFunctions()
        data = {}
        data['venueid'] = request.form['venue']
        data['username'] = session['username']
        data['eventname'] = form.eventname.data
        data['eventdesc'] = form.eventdesc.data
        data['eventdate'] = form.eventdate.data
        data['starttime'] = form.starttime.data
        data['endtime'] = form.endtime.data
        data['eventcapacity'] = form.eventcapacity.data
        data['genderoption'] = form.genderoption.data
        result = mainfunc.start_event(data)
        if result[0]==0:
            return '<h2>'+result[1]+'</h2>'
        else:
            flash(f'Event: {form.eventname.data} has been started!', 'success')
            return redirect(url_for('home'))
    return render_template("start_event.html", title="Start Event", form=form, list=venuelist)



@app.route("/venueevents", methods=['GET','POST'])
def venueevents():
    func = MainFunctions()
    print(request.form['venue'])
    result = func.display_events_for_venue_id(request.form['venue'])
    print(result[1])
    if(result[0] == 1):
        return render_template("venue_events.html", title="VenueEvents", list=result[1])
    else:
        return "<h2>"+result[1]+"</h2>"


@app.route("/editevents", methods=['GET','POST'])
def editevents():
    func = CommonFunctions()
    result = func.get_all_events()
    print(result[1])
    if(result[0] == 1):
        return render_template("event_list.html", title="Event List", list=result[1])
    else:
        return "<h2>"+result[1]+"</h2>"

@app.route("/removeevent", methods=['GET','POST'])
def removeevent():
    func = MainFunctions()
    return render_template("success_joined.html", title="Event Removed")

@app.route("/joinevent", methods=['GET','POST'])
def joinevent():
    func = MainFunctions()
    eventid=request.form['eventid']
    message = func.user_joins_event(session['userid'],eventid)
    return render_template("success_joined.html", title="Event Joined", message=message)



@app.route("/joinedgames", methods=['GET','POST'])
def joinedgames():
    func = MainFunctions()
    result = func.events_joined_user_id(session['userid'])
    print(result[1])
    if(result[0] == 1):
        return render_template("joined_games.html", title="Joined Games", list=result[1])
    else:
        return "<h2>"+result[1]+"</h2>"

@app.route("/userlist", methods=['GET','POST'])
def userlist():
    func = CommonFunctions()
    list = func.get_all_users()
    return render_template("user_list.html", title="User Directory", list=list)



@app.route("/makeadmin", methods=['GET','POST'])
def makeadmin():
    func = MainFunctions()
    # Show joined events of the user
    result = func.makeadmin_user(request.form['userid'])
    return redirect(url_for('userlist'))

@app.route("/removeuser", methods=['GET','POST'])
def removeuser():
    func = MainFunctions()
    # Show joined events of the user
    print(request.form['userid'])
    result = func.remove_user(request.form['userid'])
    if result[0]==1:
        return redirect(url_for('userlist'))
    else:
        return "<h2>"+result[1]+"</h2"

@app.route("/activateuser", methods=['GET','POST'])
def activateuser():
    func = MainFunctions()
    # Show joined events of the user
    print(request.form['userid'])
    result = func.activate_user(request.form['userid'])
    if result[0]==1:
        return redirect(url_for('userlist'))
    else:
        return "<h2>"+result[1]+"</h2"

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



