from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Listing
from django.http import Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .languages import Language, English, Espanol, Francais
from .plivo_send import response

PLIVO_NUMBER = "18058643381" # in the future will call deployment.txt

def index(request):
	print "index"
	latest_listing_list = Listing.objects.order_by('-pub_date')[:6]
	context = {'latest_listing_list': latest_listing_list,}
	return render(request, 'topmenu/index.html', context)

def detail(request, detail_id):
	print "detail"
	detail_display = get_object_or_404(Listing, pk = detail_id)
	return render(request, 'topmenu/detail.html', {'apples': detail_display})

# receieve sms method
@csrf_exempt
@require_POST
def plivo_endpoint(request):
	source = request.POST['From']
	destination = request.POST['To']
	messageuuid = request.POST['MessageUUID']
	message_content = request.POST['Text']
	message_time = datetime.now()

	try:
		User.objects.get(phone_num=source)
	except User.DoesNotExist:
		# create new User_data entry
		User.objects.create(phone_num=source, user_state=1)
		return render(request, 'topmenu/new_user.html', {'phone_num':source}),
		source # do something with this
	else:
		return menu_2(source)

def send_message(source, destination, menu_text):
	# not sure on the best way to call p.send in plivo_send
	# need to return render or httprequest?
	return response

def menu_2(phone_num):
	# update user state to reflect current menu
	current_state = User.objects.filter(phone_num).update(user_state=2)
	current_state.save()
	current_language = User.objects.filter(phone_num).get(user_language)
	menu_text = "1. %s, 2. %s, 3. %s, 4. %s" % (current_language.for_sale, 
		current_language.wanted, current_language.jobs, current_language.announcements)
	phone_num = reply_destination
	reply_source = Plivo_number
	# need to return render or httprequest?
	return send_message(reply_source, reply_destination, menu_text) 







