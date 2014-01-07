from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from gevent.greenlet import Greenlet
from django.shortcuts import render, redirect
import gevent
import random

import urllib2

def gethtml(url):
	response = urllib2.urlopen(url).read()
	#result = response.read()
	gevent.sleep(random.randint(0,2)*0.001)
	print "------------------------------------"
	print "------------------------------------"
	print url
	print "------------------------------------"
	print "------------------------------------"
	#print response
	return HttpResponse(response)

@csrf_exempt
def user(request):
	# url = request.POST['url']
	# # response = urllib2.urlopen(url)
	# # result = response.read()
	# # print result
	# # 
	# Greenlet.spawn(gethtml,url)
	# #Greenlet.join()
	# return HttpResponse("response")
	print settings.STATIC_ROOT
	print settings.STATIC_URL
	return render(request, 'user.html')