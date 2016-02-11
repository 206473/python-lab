from Login.models import User
from main.models import Subscriptions
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.sessions.backends.db import SessionStore
from django.utils.six.moves.urllib.parse import urlparse
import sys
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from main.models import Images
from django import template
def main(request):
	#return HttpResponse(request.session['user_id'])
	if not request.session.get('user_id'):
		return redirect("/")
	var = []
	for i in Subscriptions.objects.filter(user=User.objects.get(id=request.session['user_id'])):
		var.append(i.url)
	return render_to_response('main.html',{'list':var},context_instance=RequestContext(request))
def ViewImages(request):
	if not request.session.get('user_id', False):
		return redirect("/Login/")
	var = []
	var1 = []
	subscription = Subscriptions.objects.get(url=request.POST.get('subs'))
	print(subscription.url)
	print(subscription.id)
	for i in Images.objects.filter(subscribe_id=subscription.id).order_by('-id'):
		var.append(i)
		
	for i in Subscriptions.objects.filter(user=User.objects.get(id=request.session['user_id'])):
		var1.append(i.url)
	return render_to_response('main.html',{"img": var, 'list':var1},context_instance=RequestContext(request))
def subscription(request):
	if not request.session.get('user_id', False):
		return redirect("/Login/")
	if request.method=='POST':
		try:
			subs = Subscriptions.objects.get(url=request.POST.get('url'))
		except:
			subs = Subscriptions(url=request.POST.get('url'))
			subs.save()
		subs.user.add(User.objects.get(id=request.session['user_id']))
		subs.save()
		CheckUpdates(request)
		#return HttpResponse(request.POST.get('url'))
		
		return redirect('/main/main/')
def CheckUpdates(request):
	
	for subs in Subscriptions.objects.filter(user=User.objects.get(id=request.session['user_id'])):
		resp = requests.get(subs.url)
		
		print(resp)
		soup = BeautifulSoup( resp.content ,"html5lib")
		images = soup.find_all( 'img')
		for img in images:
			width, height = get_image_size(img.get( 'src' ))
			if width>200 and height>200:
				try:
					Images.objects.create(subscribe_id=subs.id,url=img.get('src'))
				except:
					continue
	return 0
def get_image_size(url):
	try:
		data = requests.get(url).content
	except:
		try:
			data = requests.get("http:"+url).content
		except:
			return 0,0
	im = Image.open(BytesIO(data))    
	return im.size
# Create your views here.
