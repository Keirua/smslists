#need to figure out a way to update user loc within postresql logic


#import sqlite3
from datetime import datetime

#conn= sqlite3.connect(':memory:')
import psycopg2

conn = psycopg2.connect('dbname=alando user=postgres')
cur = conn.cursor()
now = datetime.now()


phone_number = '123456'
while True:
	text = raw_input('')
	process_text(phone_number, text)

class user(object):
	def __init__(self, user_id, phone_num, carrier, language, jointime, loc, pos):
		self.user_id = user_id 
		self.phone_num = phone_num #searches for number, if no number is found, new user is initiated. if user is found 

		cur.execute(
			"""SELECT user_id FROM users_list WHERE phone_num = input_phone_num;""")
		cur.fetchall()


		self.carrier = carrier
		self.language = language
		self.jointime = jointime
		self.loc = loc
		self.pos = pos


# global variable class. everytime there is an user interaction, session state needs to be updated. read about flask.

def integertest(x):
	try:
	  int(x) + 1
	except ValueError:
	  return False

def top_menu_function():
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

def menu_execute(data_type): #need to test listing length. #randomize
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
			hdr_input, pr_input, des_input, psttime_input, pass)); 
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


