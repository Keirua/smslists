from django import forms

class User_data(forms.Form):
	user_phone_num = forms.CharField(label = "Phone Number", max_length=10)
	# is CharField able to capture varchars?
	user_carrier = forms.CharField(label = "Carrier", max_length=2)
	# thinking of recording carriers in 2 digits for fast DB read/write
	user_jointime = forms.CharField(label = "Jointime",)
	# what's the best format for this ^?
	user_state = forms.CharField(label = "UserState", max_length=2)
	# each menu view will be assigned a 2-digit state identifier. will need
	# to have this time out after a given amount of time
	user_loc = forms.CharField(label = "User Location")
	# In U.S., ask for zipcode. Internationally, ask for closest city.
	user_command = forms.CharField(label = "User Command", max_length=1)
	# the 0-9 commands that the user will be able to enter
	user_hdr_input = forms.Charfield(label = "User Header Input", max_length=40)
	# the text header that will be viewed when browsing listings
	user_body_input = forms.Charfield(label = "User Body Input", max_length=140)
	# the text body of any listing
	user_image_input = 
	# 
