
import psycopg2
conn=psycopg2.connect('dbname=alando user=postgres')
cur = conn.cursor()

from datetime import datetime
now = datetime.now()

for_sale_menu = cur.execute("SELECT * FROM for_sale_list;")

wanted_menu = {}
jobs_menu = {}
announcements_menu = {}
discussion_menu = {}

def menu_execute(x):
	cur.execute("SELECT fslid, header, price, FROM %s ORDER BY timestamp DESC LIMIT 4"), (x) #might need to adjust format of timestamp to make ordering work. also will need to replace "fslid" w/ value for all listings
	cur.fetchall()
	#FORMATTING GOES HERE
	#PRINT LIMITING THAT KEEPS RESPONSE TO 160-CHARACTER PAGES GOES HERE (WRITE EXPRESSION TO SUBSTITUTE FOR 4?^)
	#NEED TO FIGURE OUT HOW TO ASSIGN LISTING NUMBERS TO SQL QUERY
	menu_execute_input = raw_input("Reply with listing id to view a listing and 'post' to post a new listing.") #see previous note
	if menu_execute_input == 'post':
		new_listing_add(activelist)
	cur.execute("SELECT menu_execute_input FROM activelist;") #need to make listing id the primary key. also need to verify that this method will work for returning individual entry.


def nlidfunction(activelist):
	cur.execute("SELECT COUNT(*) FROM activelist;")
	fetch_count_raw = str(cur.fetchall()) #should this be .fetchlast() instead?
	new_fetch_count_raw1 = fetch_count_raw.replace("L,)]", "")
	new_fetch_count = new_fetch_count_raw1.replace("[(", "")
	nlid = int(new_fetch_count)+1

def new_listing_add(activelist):
	header_text = raw_input("In 20 characters or less, please describe, 'What do you want to list?'")
	if len(header_input) > 20:
		print "Your entry exceeded the 20-character limit. The following is the first 20 characters of your entry: "+header_text[:20]
		header_text = raw_input("In 20 chaacters or less, please describe, 'What do you want to list?'")
	price_input = raw_input("How much will you sell it for?")
	if integertest(price) == false or len(price) > 6:
		print "Your price entry was either not a number or exceeded the maximum length of 6 chacacters. The following is the first 6 characters of your entry: "+price[:6]
		price = raw_input("How much will you sell it for?")
	listing_description = raw_input("In 100 characters or less, describe your listing.")
	if len(listing_description) > 100:
		print "Your entry exceeded the 100-chacter limit. The following is the first 100 characters of your entry: "+listing_description[:100]
		listing_description = raw_input("In 100 characters or less, describe your listing.")

	cur. execute(
		"""INSERT INTO %s (%s, %s, %s, %s, %s, %s) 
		VALUES (%s, %s, %s, %s, %s, %s);""", (activelist, fslid, header, price, description, user_id, timestamp, nlidfunction(activelist), header_input, price_input, listing_description, getuserid(), now)
	conn.commit()

def get_userid(phone_number):
	cur.execute("SELECT") #comes from texting api

	cur.execute(
		"""INSERT INTO users_list (id, phone_number, carrier, jointime) 
		VALUES (%s, %s, %s, %s);""",
		(new_user_id, new_user_phone, new_user_carrier_string, new_user_jointime))
	conn.commit()

		cur.execute("SELECT COUNT(*) FROM users_list;")
		fetch_count_raw = str(cur.fetchall()) #should this be .fetchlast() instead?
		new_fetch_count_raw1 = fetch_count_raw.replace("L,)]", "")
		new_fetch_count = new_fetch_count_raw1.replace("[(", "")
		new_user_id = int(new_fetch_count)+1
		new_user_jointime = now


def integertest(x):
	try:
  	  int(x) + 1
	except ValueError:
  	  return False

def new_user():
	
	new_user_phone = raw_input("Welcome! Enter your phone number: ")
	if integertest(new_user_phone) == False or len(str(new_user_phone)) != 10:
		print "Number not recognized or did not contain 10 digits."
		new_user()
	else:
		new_user_phone_check = True 
		print "Your phone number was recorded as "+new_user_phone+", thanks!"
	
	def carrier_entry():
	new_user_carrier = raw_input("Which carrier do you use? Reply '1' for ATT '2' for Verizon. ")
	if int(new_user_carrier) == 1:
		new_user_carrier_check = True
		new_user_carrier_string = "ATT" 
		print "Your carrier was recorded as "+new_user_carrier_string+". Thanks!"
	elif int(new_user_carrier) == 2:
		new_user_carrier_check = True
		new_user_carrier_string = "Verizon"
		print "Your carrier was recorded as "+new_user_carrier_string+". Thanks!"
	else:
		if int(new_user_carrier) != 1 or 2:
			print "Input not recognized. Please reply '1' if your wireless carrier is ATT and '2' if your wireless carrier is Verizon."
			carrier_entry()

	if 	new_user_phone_check == True and new_user_carrier_check == True:
		cur.execute("SELECT COUNT(*) FROM users_list;")
		fetch_count_raw = str(cur.fetchall()) #should this be .fetchlast() instead?
		new_fetch_count_raw1 = fetch_count_raw.replace("L,)]", "")
		new_fetch_count = new_fetch_count_raw1.replace("[(", "")
		new_user_id = int(new_fetch_count)+1
		new_user_jointime = now
	else:
		print "Error 1"


	cur.execute(
		"""INSERT INTO users_list (id, phone_number, carrier, jointime) 
		VALUES (%s, %s, %s, %s);""",
		(new_user_id, new_user_phone, new_user_carrier_string, new_user_jointime))
	conn.commit()

def menus():
	top_menu = raw_input("Reply: '1' For sale, '2' Wanted, '3' Jobs, '4' Announcements, '5' Discussion.")
	if int(top_menu) == 1:
		activelist = for_sale_listings
		menu_execute(activelist)
	elif int(top_menu) == 2:
		activelist = wanted_listings
		menu_execute(activelist)
	elif int(top_menu) == 3:
		activelist = jobs_listing
		menu_execute(activelist)
	elif int(top_menu) == 4:
		activelist = announcements_listings
		menu_execute(activelist)
	elif int(top_menu) == 5:
		activelist = discussion_listings
		menu_execute(activelist)
	else:
		return "Input not recognized."
		menus()

print new_user()
print menus()
