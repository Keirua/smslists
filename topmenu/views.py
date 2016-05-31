from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Listing
from django.http import Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
now = datetime.now()


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
		User_data.objects.get(phone_num=source)
	except (User_data.DoesNotExist):
		# create new User_data entry 
		new_user = User_data(user_id(), phone_num=source, user_jointime=now, 
			user_state=1, user_sms_quant =1,)
		# does the AutoField user_id need an arg?
		new_user.save()
		return render(request, 'topmenu/new_user.html', {'phone_num':source})
	else:
		return menu_2(phone_num)

def send_message(src, dest, text):
	pass


def menu_2(phone_num):
	# update user state to reflect current menu
	current = User_data.objects.filter(phone_num).update(user_state=2)
	current.save()
	pass #main menu showing 1. for sale 2. wanted 3. jobs 4. announcements








