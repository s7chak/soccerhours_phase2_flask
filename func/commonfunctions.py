import datetime
import os
import pymysql


class CommonFunctions():
    

    def db_connection(self):
        db_user = os.environ.get('CLOUD_SQL_USERNAME')
        db_password = os.environ.get('CLOUD_SQL_PASSWORD')
        db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
        db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
        else:
            host = '127.0.0.1'
            cnx = pymysql.connect(user='root', password='root1234', host=host, db='soccerhoursdb')
            
        return cnx


    # Duplicate UserName check
    def dup_username_check(self,username):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' SELECT username from user ''')
            usernames=cursor.fetchall()
            if ((username,) in usernames):
                print("UserName {0} already exists.".format(username))
                return False
            else:
                print("Username available, please proceed.")
                return True




    # Duplicate Email check
    def dup_email_check(self,email):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' SELECT user_email from user ''')
            emails=cursor.fetchall()
            if (email,) in emails:
                print("User with email address {0} already exists.".format(email))
                return False
            print("Unique email address, please proceed.")
            return True




    # Duplicate Venue check
    def dup_venue_check(self,venuename,zipcode):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' SELECT venue_name, venue_zip_code from venue ''')
            venues=cursor.fetchall()
            venue=(venuename,zipcode)

            if (venue in venues):
                print("Venue with name: \'{0}\' and Zip code: {1} already exists.".format(venuename,zipcode))
                return False
            else:
                return True




    # Function to get slot IDs from start and end times
    def get_slot_ids(self,starttime, endtime):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            diff = endtime - starttime
            slotstarts=starttime
            cursor.execute(''' SELECT slot_id from timeslots where start_time= %s ''',[starttime])
            slotids=[]
            slotids.append(cursor.fetchone()[0])
            
            if diff>1:
                for i in range(diff-1): 
                    slotids.append(slotids[i]+1)
            return slotids 




    #Function to check validity of date, by identifying dates as 'G' for future dates, 'L' for past dates and 'T' for today.
    def check_valid_date(self,date):
        today=str(datetime.datetime.today()).split()[0]
        if (date>today):
            return 'G'
        elif(today>date):
            return 'L'
        else:
            return 'T'
        



    # Function to check validity of time entered for the current day
    def check_valid_time_today(self,starttime):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            now = datetime.datetime.now()
            if (now.hour >= int(starttime)):
                return False
            else:
                return True




    # Function to check invalid start and end times
    def check_start_end_time(self,time,startorend):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            now = datetime.datetime.now()
            inttime=int(time)
            if (startorend=='S'):
                if (inttime<8 or inttime>20):
                    return False
                else:
                    return True
            else:
                if (inttime<8 or inttime>21):
                    return False
                else:
                    return True  




    # Function to check if Slots table is populated
    def check_venue_slots(self,venueid, eventdate):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' Select 1 from slots where venue_id=%s and date=%s ''',[venueid,eventdate])
            if cursor.fetchone()!=None:
                return 'P'
            return 'N'
            



    # Fucntion to check if given slots are already booked
    def check_slots_booked(self,venueid, eventdate, slotids):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            query="Select count(1) from slots where venue_id={0} and date=\'{1}\' and availability=\'U\' ".format(venueid,eventdate,slotids)
            query=query+"and slot_id in (" + ",".join((str(n) for n in slotids)) + ")"

            cursor.execute(query)
            num = cursor.fetchone()[0]
            if num>0:
                return True
            return False




    #Function to check if an user exists
    def check_valid_user(self,userid):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' Select pk_user_id from user where pk_user_id=%s ''',[userid])
            user=cursor.fetchone()
            if(user!=None):
                return True
            return False
  
    #Function to check if an user exists
    def check_admin_user(self,userid):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' Select admin_statusfrom user where pk_user_id=%s ''',[userid])
            user=cursor.fetchone()
            if user[0]=='A':
                return True
            return False



    # Function to check if a venue exists
    def check_valid_venue(self,venueid):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' Select pk_venue_id from venue where pk_venue_id=%s ''',[venueid])
            venue=cursor.fetchone()
            if venue:
                return True
            return False




    # Function to check if an event exists
    def check_valid_event(self,eventid):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' Select pk_event_id from events where pk_event_id=%s ''',[eventid])
            event=cursor.fetchone()
            if(event!=None):
                return True
            return False




    # Function to check the validity of date format
    def validate_date(self,date):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            try:
                datetime.datetime.strptime(date, '%Y-%m-%s')
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")


    # Function to check the validity of date format
    def get_all_venues(self):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' Select pk_venue_id, venue_name from venue ''')
            return cursor.fetchall()

    def get_all_users(self):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            cursor.execute(''' Select pk_user_id, username, user_fname, user_lname, user_status, admin_status from user ''')
            return cursor.fetchall()


    def get_all_events(self):
        connection = self.db_connection()
        with connection.cursor() as cursor:
            query='SELECT e.event_name, v.venue_name, e.event_date, e.start_time, e.end_time, (e.event_capacity - e.members_joined), e.pk_event_id, e.event_status FROM events e JOIN venue v ON e.venue_id=v.pk_venue_id'
            cursor.execute(query)
            eventlist=cursor.fetchall()
            response=list()
            print(eventlist)
            for event in eventlist:
                date_time = event[2].strftime("%m-%d-%Y")
                elem=list()
                elem.append(event[0])
                elem.append(event[1])
                elem.append(date_time)
                elem.append(str(event[3])+":00")
                elem.append(str(event[4])+":00")
                elem.append(event[5])
                elem.append(event[6])
                elem.append(event[7])
                response.append(elem)
                print(elem)
            
            connection.close()
            if (eventlist is not None):
                return (1,response)
            else:
                return (0,"No events currently booked.")

