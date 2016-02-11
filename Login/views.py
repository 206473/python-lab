from Login.models import User
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import psycopg2
def index(request):
	
	c = {}
	if request.method == 'POST':
		login = request.POST.get('login')
		password = request.POST.get('password')
		email = request.POST.get('email')
		try:
			user = User.objects.get(email=email, password=password);
			request.session['user_id']=user.id
			return redirect('/main/main/', request)
		except:
			return HttpResponse('Пользователь не найден!')
	else:
		return render_to_response('login.html',{},context_instance=RequestContext(request))
def logout(request):
	request.session.clear()
	return redirect("/")
 