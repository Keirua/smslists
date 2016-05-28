#sqlite implementation
#import sqlite3
#conn= sqlite3.connect(':memory:')
########
#only psycopg2
#import psycopg2
#conn = psycopg2.connect('dbname=alando user=postgres')
#cur = conn.cursor()
########
# heroku db settings

import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["https://git.heroku.com/heroku-postgres-4ba0b50c.git"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

#psycopg2+sqlalchemy implementation


from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://user:postgres@host:5432/alando')
	#[?key=value&key=value...]) #keyword arguments optional
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Varchar
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

from datetime import datetime
now = datetime.now()

class User(Base):
	__tablename__='users_list'

	id = Column(Integer, primary_key=True) # eed Serial for Postgres?
	phone_num = Column(Varchar)
	carrier = Column(Integer)
	language = Column(Integer)
	jointime = Column(Integer) # test, but Int seems to make most sense
	loc = Column(Varchar) # format may change region-to-region
	pos = Column(Integer) # need to assign int values to each menu screen
	acttime = Column(Integer) # ∆time since last activity

	def __repr__(self):
		return """<User(phone_num='%s', carrier='%s', language='%s',
			jointime='%s', loc='%s', pos='%s', acttime='%s')>""" % (
							self.phone_num, self.carrier, self.language
							self.jointime, self.loc, self.pos, self.acttime)

Base.metadata.create_all(engine)

input_phone_numr = #from Plivo
while True:
	text = raw_input('')
	process_text(input_phone_num, text)

session.query(User).filter_by(phone_num='%s').first() % (input_phone_num)
# ^search db to see if phone_num is already listed.
# if search returns null, call new_user_funtion_input()
# else, call top_menu_function

# from clark -> global variable class. everytime there is an user interaction,
# session state needs to be updated. read about flask.

def integertest(x):
	try:
	  int(x) + 1
	except ValueError:
	  return False

def top_menu_function():uuuu
	user.pos = "top_menu_function"
	while True:
		try:
			top_menu = int(raw_input("""Reply '1' For Sale, '2' Wanted, '3' 
				Jobs, '4' Announcements"""))
		except ValueError:
			print """Input not recognized. Please reply with a number between 
				1-4."""
			continue

			if str(top_menu) != '1' or str(top_menu) != '2' or str(top_menu) !='3' or str(top_menu) != '4':
			new_user_carrier = raw_input("""Sorry, input not recognized.""") #seems similar to what wasn't working before
			continue
		else:
			break

	while True:
		if top_menu == 1:
			return data_type = 1
			break
		elif top_menu == 2:
			return data_type = 2
			break
		elif top_menu == 3:
			return data_type = 3
			break
		elif top_menu == 4:
			return data_type = 4
		break

def menu_execute(data_type): # need to test listing length. #randomize
	user.pos = str(data_type)
	cur.execute(
		"""SELECT ls_id, ls_hdr, ls_pr, FROM listings WHERE ls_type == %s 
			ORDER BY ls_psttime DESC LIMIT 4;""", (data_type)) #after 
			#connecting cell tower api, need algorithm that will order by 
			#ls_psttime, ls_loc
	cur.fetchall()

	menu_execute_input = raw_input("""Reply with listing id to view a listing 
		and 'post' to post a new listing.""")

	if menu_execute_input = pass #how to call specific primary key from fetchall() of ^ ?
		
	elif menu_execute_input == 'post':
		new_listing_add(data_type)

def new_listing_add(x):
	user.pos = "new_listing_add"
	while True:
		hdr_input = raw_input("""In 20 characters or less, please describe, 
		'What do you want to list?'""")
		if len(hdr_input) > 20:
			print """Your entry exceeded the 20-character limit. The following
			 is	the first 20 characters of your entry: """+hdr_input[:20]
			break	
	
	while True:
		pr_input = raw_input("How much will you sell it for?")
		if integertest(pr_input) == false or len(price) > 6:
			print """Your price entry was either not a number or exceeded the 
			maximum length of 6 chacacters. The following is the first 6 
			characters of your entry: """+price[:6]
			break
	
	while True:
		des_input = raw_input("""In 100 characters or less, 
			describe your listing.""")
		if len(des_input) > 100:
			print """Your entry exceeded the 100-chacter limit. The following is 
			the first 100 characters of your entry: """+des_input[:100]
			break

	psttime_input = now

	loc_input = pass #API CALL

		#need to connect to api and build user_id finder.
		#also need the execute statement below to pull loc logic.

	cur.execute(
		"""INSERT INTO listings (ls_type, ls_hdr, ls_pr, ls_des, user_id, 
			ls_psttime, ls_loc) VALUES (%s, %s, %s, %s, %s, %s, %s);""", (data_type, 
			hdr_input, pr_input, des_input, psttime_input, pass)) 
	conn.commit()

def new_user_function_input():
	user.pos = "new_user_function_input"
	while True:
		try:
			new_user_phone = raw_input("Welcome! Enter your phone number: ")
			new_user_phone_tst1 = int(new_user_phone)
		except ValueError:
			print("""Sorry, a phone number can only consist of numbers. Please
				enter only your 10-digit phone number without any spaces 
				or symbols.""") #could potentially be replaced via api integration
			continue

		if len(new_user_phone) != 10:
			print """Phone number was an incorrect number of characters. Please 
				enter only your 10-digit phone number without any spaces or 
				symbols."""
			continue
		else:
			break

	new_user_carrier = raw_input("""Which carrier do you use? Reply 
			'1' for ATT '2' for Verizon.""")
	while new_user_carrier != '1' and new_user_carrier != '2':
		new_user_carrier = raw_input("""Sorry, input not recognized.""")

	if int(new_user_carrier) == 1:
		new_user_carrier_string = 'ATT'
		
	if int(new_user_carrier) == 2:
		new_user_carrier_string = 'Verizon'

	
	print "Your phone number was recorded as "+new_user_phone+""". Your 
			carrier was recorded as """+new_user_carrier_string+""". Thanks
			and welcome to txtlists!"""
	
	phone_num_v = new_user_phone
	carrier_v = new_user_carrier
	jointime_v = str(now)

	cur.execute(
	"""INSERT INTO users_list (phone_num, carrier, jointime) 
	VALUES (%s, %s, %s);""", (phone_num_v, carrier_v, jointime_v))
	conn.commit()

new_user_function_input() #need control flow -> if not a new user, call 
#top_menu_function() first
top_menu_function()

menu_execute(activelist)

def process_text(phone_number, text):
	???






####################################################

#sign_up_new_user():
#    while True
#        get_phone_number()
#        if validate_phone(phone_number): break
#    while True
#        get_carrier()
#        if validate_carrier(carrier): break

#class Validator():
#    def __init__(self):
#        pass
#    def phone_numer(self,num):
#        pass
#    def carrier(self,carrier):
#        pass
#    def other_thing_needing_validation(self, thing)


