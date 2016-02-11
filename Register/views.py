from Login.models import User
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.http import HttpResponse
import psycopg2
def index(request):
	c = {}
	if request.method == 'POST':
		logins = request.POST.get('login')
		passwords = request.POST.get('password')
		emails = request.POST.get('email')
		
		try:
			conn = psycopg2.connect("dbname='laba' user='postgres' host='localhost' password='root' port='5432'")
		except:
			print("I am unable to connect to the database")
		else:
			try:
				try:
					user = User.objects.get(login=logins, email=emails)
					return HttpResponse('Пользователь уже существует!')
				except:
					user = User(login=logins, password=passwords, email=emails);
					user.save()
					return redirect('/');
			except:
				#user=1
				return HttpResponse("Error!")
	else:
		return render_to_response('register.html',{},context_instance=RequestContext(request))
 