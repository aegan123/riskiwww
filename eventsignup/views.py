from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse
#from .models import TapahtumaTyypit, TapahtumanOmistaja, Tapahtumat, Sitsit, Vuosijuhla, Ekskursio
#from .models import MuuTapahtuma, Osallistuja, Arkisto
#from django import forms
from eventsignup.forms import SitzSignupForm, AnnualfestForm, ExcursionForm, OtherEventForm, CustomForm, SelectTypeForm, SitzForm
#from omat import helpers
import random

def index(request):
	#kts tutoriaali!! template tms
	#return render(request,'eventsignup/info.html',{'info':info})
#	form = SitzSignupForm()
	return render(request, "eventsignup/index.html")
	#return HttpResponse("Welcome!")

#sivupaneelin nippelitieto
@login_required
def stats(request, uid):
	pass

def signup(request, uid):
	#return HttpResponse(filter(str.isdigit, request.path))
	return HttpResponse(uid)
#	if(request.method == 'POST'):
		#tee jotain
#		tyyppi=get_object_or_404(Tapahtumat, uid=uid)
#		form = SitsitSignupForm(request.POST)
#		if(form.is_valid()):
			#käsittele lomake
#	else:
#		form = SitsitSignupForm()
#	return render(request, "eventsignup/new_event.html", {'form': form})

@login_required
def archive(request, uid):
	pass

@login_required
def add(request,**kwargs):
	if kwargs:
		return HttpResponse(kwargs['type'])
	if(request.method=='POST'):
		uid=random.randint(10000, 99999)
		#käsittele lomake
		form=SelectTypeForm()
	else:
		form=SelectTypeForm()
	return render(request,"eventsignup/new_event.html",{'form':form})

@login_required
def formtype(request,eventtype):
#	sitsit, vujut, eksku, muu, custom
	if(request.method=='POST'):
		return HttpResponseNotAllowed(['GET',''])
	if(eventtype=='sitsit'):
		form = SitzForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	elif(eventtype=='vujut'):
		form = AnnualfestForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	elif(eventtype=='eksku'):
		form = ExcursionForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	elif(eventtype=='muu'):
		form = OtherEventForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	elif(eventtype=='custom'):
		form = CustomForm()
		return render(request, "eventsignup/new_event.html", {'form': form})
	else:
		return HttpResponseBadRequest()

@login_required
def info(request, uid):
	pass

@login_required
def management(request):
	return HttpResponse("Foobar")

@login_required
def edit(request):
	pass


