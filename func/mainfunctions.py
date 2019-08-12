import datetime
import time
from .commonfunctions import CommonFunctions as common
import os
import pymysql

class MainFunctions():

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


	# Adds One New user by inserting into table 'user'
	def add_user(self,userdata):
		connection = self.db_connection()
		with connection.cursor() as cursor:

			username=userdata['username']
			firstname=userdata['firstname']
			lastname=userdata['lastname']
			email=userdata['email']
			password=userdata['password']
			zipcode=userdata['zipcode']
			isadmin=userdata['isadmin']
			
			print(userdata)
			now=datetime.datetime.now()
			now=now.strftime('%Y-%m-%d')

			cursor.execute(''' INSERT INTO user VALUES((select seq from sqlite_sequence where name='user')+1,%s,%s,%s,%s,'I',%s,%s,%s,%s) ''',[firstname,lastname,username,isadmin,email,password,int(zipcode),now])
			cursor.execute(''' UPDATE sqlite_sequence set seq=seq+1 where name=\'user\' ''')
			connection.commit()
			connection.close()
			if cursor.rowcount == 1:
				return 1
			else:
				return 0

	# Login function
	def log_in(self,userdata):
		connection = self.db_connection()
		with connection.cursor() as cursor:

			username=userdata['username']
			password=userdata['password']
			print(username)

			cursor.execute('SELECT username, user_password, admin_status, user_status, pk_user_id from user where username=%s',[username])
			row = cursor.fetchone()
			if row != None:
				user=row[0]
				passw=row[1]
			else:
				return HttpResponse("<h2 align='center'>Sorry user:%s does not exist. Please retry logging in.</h2>" % username)

			connection.close()
			if user == username and passw == password:
				return [1,row[2],row[3], row[4], row[0]]
			else:
				return [0]


	def get_venues_for_slot(self,starttime, endtime, date):
		connection = self.db_connection()
		with connection.cursor() as cursor:
			c = common()
			if c.check_start_end_time(starttime,'S') and c.check_start_end_time(endtime,'E'):
				slotids=c.get_slot_ids(int(starttime),int(endtime))
			else:
				print("\nInvalid timings entered. Venue not booked.\n\nValid values are : \nRange of 8 - 20 for Start time\nRange of 9 - 21 for End time")
				return None

			print ("\n\nThe Venues that have %s => %s Slots available:" % (starttime, endtime))

			print(slotids)
			query='SELECT distinct s.venue_id, v.venue_name from slots s join venue v on v.pk_venue_id=s.venue_id where venue_id not in (SELECT distinct venue_id from slots where availability =\'U\' and slot_id in (' + ','.join((str(n) for n in slotids)) + ') and date=\'%s\') UNION SELECT distinct v.pk_venue_id, v.venue_name from venue v where pk_venue_id not in (SELECT venue_id from slots)' % date
			cursor.execute(query)
			
			venuesforslot=cursor.fetchall()

			return venuesforslot



	# Adds the New Event by inserting into table 'events'
	def start_event(self,eventdata) :
		connection = self.db_connection()
		with connection.cursor() as cursor:
			c = common()
			venueid=eventdata['venueid']
			username=eventdata['username']
			eventname=eventdata['eventname']
			eventdesc=eventdata['eventdesc']
			eventdate=eventdata['eventdate']
			starttime=eventdata['starttime']
			endtime=eventdata['endtime']
			eventcapacity=eventdata['eventcapacity']
			genderoption=eventdata['genderoption']
			if (c.check_start_end_time(starttime,'S')==False and c.check_start_end_time(endtime,'E')==False):
				# Derive slots from StartTime, EndTime
				print("\nInvalid timings entered. Venue not booked.\n\nValid values are : \nRange of 8 - 20 for Start time\nRange of 9 - 21 for End time")
				return
			else:
				slotids=[]
				slotids=c.get_slot_ids(int(starttime),int(endtime))
				
			cursor.execute(''' Select seq+1 from sqlite_sequence where name='events' ''')	
			eventid=cursor.fetchone()[0]
			
			datestatus=c.check_valid_date(eventdate)
			if(datestatus=='G' or datestatus=='T'):
				if(datestatus=='T' and ~c.check_valid_time_today(starttime)):
					print("For today time(Hour) needs to be greater than now. Please retry.")
					return (0,"For today time(Hour) needs to be greater than now. Please retry.")
				else:	
					# Check if entries exist in Slots
					slotspresent = c.check_venue_slots(venueid, eventdate)
					if(c.check_slots_booked(venueid, eventdate, slotids)):
						print("The entered slot(s) are already booked.")
						return (0,"The entered slot(s) are already booked.")
					if slotspresent=='N':
						print("Inserting...")
						for i in range(13):
							cursor.execute(''' INSERT INTO slots VALUES(%s+1,%s,%s,'A',%s) ''',[i,venueid,eventdate,eventid])
							connection.commit()
					for i in slotids:
						cursor.execute(''' Update slots set availability='U', event_id=%s where venue_id=%s and slot_id=%s and date=%s''',[eventid,venueid,i,eventdate])
					
					cursor.execute(''' SELECT pk_user_id from user where username= %s ''',[username])
					useridresult = cursor.fetchone()
					if useridresult:
						userid = useridresult[0]
					else:
						return (0,"User ID not found for user:"+username)
					cursor.execute(''' INSERT INTO events(pk_event_id,event_name,event_desc,event_date,start_time,end_time,user_id,venue_id,event_capacity,event_status,members_joined,gender_option) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,'A',1,%s) ''',[eventid,eventname,eventdesc,eventdate,starttime,endtime,userid,venueid,eventcapacity,genderoption])
					cursor.execute(''' UPDATE sqlite_sequence set seq=seq+1 where name='events' ''')
					# Insert entry in event_members
					cursor.execute(''' INSERT INTO event_members VALUES(%s,%s) ''',[eventid,userid])
					connection.commit()
					print("Slots booked for time:",starttime,":00  to ",endtime,":00  on date:",eventdate," for Venue ID:",venueid)
					return (1," ".join(["Slots booked for time:",str(starttime),":00  to ",str(endtime),":00  on date:",eventdate," for Venue ID:",str(venueid)]))
			else:
				print("The provided date has passed. Unable to book event for past date.")
			
			connection.close()





	def user_joins_event(self,userid, eventid) :
		connection = self.db_connection()
		with connection.cursor() as cursor:
			c = common()
			if c.check_valid_user(userid) is False:
				print("Invalid UserID."+str(userid))
				return "Invalid UserID."
			if c.check_valid_event(eventid) is False:
				print("Invalid EventID.")
				return "Invalid Event."
			
			cursor.execute(''' Select event_capacity, members_joined from events where pk_event_id=%s ''', [eventid])
			eventroom=cursor.fetchone()

			if eventroom[0]>eventroom[1]:
				# Update Events table
				cursor.execute(''' Update events set members_joined=members_joined+1 where pk_event_id=%s ''', [eventid])

				# Update EventMembers table
				cursor.execute(''' INSERT INTO event_members values (%s,%s) ''',[eventid, userid])
				connection.commit()
				print("UserID: {0} has joined event: {1}".format(userid,eventid))
				return "You have joined an event."
			else:
				return "Sorry, but the event is full"

			connection.close()





	def get_venues_for_zipcode(self,zipcode):
		connection = self.db_connection()
		with connection.cursor() as cursor:
			query='SELECT v.venue_name, v.venue_st_addr, v.venue_zip_code, v.pk_venue_id FROM venue v where venue_zip_code = %s'
			cursor.execute(query,zipcode)
			venuesforzipcode=cursor.fetchall()
			connection.close()
			
			if (venuesforzipcode is not None):
				return venuesforzipcode
			else:
				return 0


	def add_venue(self,venuedata):
		connection = self.db_connection()
		with connection.cursor() as cursor:
			venuename=venuedata['venuename']
			venuedesc=venuedata['venuedesc']
			venueaddr=venuedata['venueaddr']
			zipcode=venuedata['zipcode']
			cursor.execute(''' INSERT INTO venue VALUES((Select seq+1 from sqlite_sequence where name='venue'),%s,%s,%s,%s) ''',(venuename,venuedesc,venueaddr,zipcode))
			cursor.execute(''' UPDATE sqlite_sequence set seq=seq+1 where name=\'venue\' ''')
			connection.commit()
			connection.close()
			if cursor.rowcount == 1:
				return 1
			else:
				return 0



	def display_events_for_zipcode(self, zipcode) :
		connection = self.db_connection()
		with connection.cursor() as cursor:
			query1='SELECT e.event_name, e.event_date, v.venue_name, e.start_time, e.end_time, e.pk_event_id FROM events e JOIN venue v ON e.venue_id=v.pk_venue_id WHERE venue_id IN (SELECT pk_venue_id from venue where venue_zip_code = %s)' %zipcode
			cursor.execute(query1)
			venuesforzipcode=cursor.fetchall()

			return venuesforzipcode
		


	def display_events_for_venue_id(self, venue_id) :
		connection = self.db_connection()
		with connection.cursor() as cursor:
			query='SELECT  e.event_date, e.event_name, v.venue_name, e.start_time, e.end_time, e.pk_event_id FROM events e JOIN venue v ON e.venue_id=v.pk_venue_id WHERE venue_id = %s'
			cursor.execute(query, venue_id)
			eventlist=cursor.fetchall()
			response=list()
			for event in eventlist:
				date_time = event[0].strftime("%m-%d-%Y")
				response.append(date_time)
				response.append(event[1])
				response.append(event[2])
				response.append(str(event[3])+":00")
				response.append(str(event[4])+":00")
				
			connection.close()
			if (eventlist is not None):
				return (1,eventlist)
			else:
				return (0,"No events at selected venue.")

	def events_joined_user_id(self, user_id) :
		connection = self.db_connection()
		with connection.cursor() as cursor:
			print(user_id)
			query='SELECT  e.event_date, e.event_name, v.venue_name, e.start_time, e.end_time, e.pk_event_id FROM events e JOIN venue v ON e.venue_id=v.pk_venue_id  JOIN event_members em ON  e.pk_event_id=em.event_id WHERE em.user_id = %s'
			cursor.execute(query, user_id)
			eventlist=cursor.fetchall()
			response=list()
			elem=list()
			for event in eventlist:
				date_time = event[0].strftime("%m-%d-%Y")
				elem.append(date_time)
				elem.append(event[1])
				elem.append(event[2])
				elem.append(str(event[3])+":00")
				elem.append(str(event[4])+":00")
				response.append(elem)
				
			connection.close()
			if (eventlist is not None):
				return (1,response)
			else:
				return (0,"No events joined by this user.")



	def remove_user(self, user_id):
		connection = self.db_connection()
		with connection.cursor() as cursor:
			query='''UPDATE user SET user_status='U' WHERE pk_user_id=%s'''
			cursor.execute(query, user_id)
			connection.commit()			
			connection.close()
			if cursor.rowcount==1:
				return (1, "User with userid:"+user_id+" has been deactivated")
			else:
				return (0,"Failed to deactivate user or you tried to make an deactivate an Inactive user.")


	def activate_user(self, user_id):
		connection = self.db_connection()
		with connection.cursor() as cursor:
			query='''UPDATE user SET user_status='A' WHERE pk_user_id=%s'''
			cursor.execute(query, user_id)
			connection.commit()			
			connection.close()
			if cursor.rowcount==1:
				return (1, "User with userid:"+user_id+" has been activated")
			else:
				return (0,"Failed to Activate user or you tried to make an activate an Active user.")

	def makeadmin_user(self, user_id):
		connection = self.db_connection()
		with connection.cursor() as cursor:
			query='''UPDATE user SET admin_status='A' WHERE pk_user_id=%s'''
			cursor.execute(query, user_id)
			connection.commit()			
			connection.close()
			if cursor.rowcount==1:
				return (1, "User with userid:"+user_id+" has been activated")
			else:
				return (0,"Failed to make user Admin or you tried to make an Admin user as Admin.")


