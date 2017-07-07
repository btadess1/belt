# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User, WishList, Joint
from django.shortcuts import render,redirect, HttpResponse
import re
from django.core.validators import validate_email
from django.contrib import messages
from datetime import datetime

# Create your views here.
def index(request):
	return render(request, 'travel_app/index.html')

def register(request):
	user = User.userManager.register(request.POST['name'], request.POST['username'], request.POST['password'], 
	request.POST['confirm'], request.POST['hire_date'])
	if user[0]:
		request.session['user_name'] = user[1].name
		request.session['user_id'] = user[1].id
		return redirect('/to_travel_plans')
	else:
		for message in user[1]:
			messages.add_message(request, messages.ERROR, message)
		return redirect('/')

def login(request):
	user = User.userManager.login(request.POST['username'], request.POST['password'])
	print user[1]
	if user[0]:
		user = User.userManager.get(username= request.POST['username'])
		request.session['user_name'] = user.name
		request.session['user_id'] = user.id
		return redirect('/to_travel_plans')
	else:
		for message in user[1]:
			messages.add_message(request, messages.ERROR, message)
		return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def to_travel_plans(request):
	this_user = User.userManager.get(id=request.session['user_id'])
	userwish = WishList.objects.filter(user=this_user)
	context ={
		'usertrip':userwish,
		'others':WishList.objects.exclude(user=this_user)
	}
	return render(request, 'travel_app/travelplans.html', context)

def to_add_travel_plan(request):
		return render(request, 'travel_app/addtravelplans.html')

def add_plan(request, id):
	if request.method == 'POST':
		messagesp = []
		if len(request.POST['item']) > 3 :
			this_user = User.userManager.get(id= id)
			this_wish =WishList.objects.create(user=this_user, item=request.POST['item'])
			#print request.POST['item']
			Joint.jointManager.create(user=this_user, wishlist=this_wish)
			request.session['wish_id'] = this_wish.id
			return redirect('/to_dashboard')
		else:
			messagesp.append('The Item/Product field is required')
			for message in messagesp:
				messages.add_message(request, messages.ERROR, message)
			return redirect('/to_add_travel_plan')

def to_dashboard(request):
	this_user = User.userManager.get(id=request.session['user_id'])
	this_wish = WishList.objects.get(id=request.session['wish_id'])
	joints = Joint.jointManager.all().filter(wishlist__id=this_wish.id)
	context ={
		'user':this_user.name,
		'this_wish':this_wish,
		'joints':joints
	}
	return render(request, 'travel_app/dashboard.html', context)

def join(request, id, idt):
	this_user = User.userManager.get(id= id)
	this_wish = WishList.objects.get(id=idt)
	this_wish.user = this_user
	this_wish.save()
	return redirect('/to_travel_plans')
	
def to_trips(request, idt, id):
	user = User.userManager.get(id=id)
	wish = WishList.objects.get(id= idt)
	joints = Joint.jointManager.all().filter(wishlist__id=idt).exclude(user=user)
	print joints
	context = {
		'trip':wish,
		'user':user,
		'joints':joints
	}
	return render(request, 'travel_app/trip.html', context)

def remove(request, id, idt):
	WishList.objects.get(id=idt).delete()
	return redirect('/to_travel_plans')

