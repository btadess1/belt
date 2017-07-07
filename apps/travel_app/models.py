# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
	def register(self, name, username, password, comfirmpass, hire_date):
		now = datetime.now()
		try:
			start_date = datetime.strptime(hire_date, '%Y-%m-%d')
		except:
			start_date = now
		messages =[]
		if len(name) < 1:
			messages.append('name is required')
		if len(username) < 1:
			messages.append('username is required')
		elif len(User.userManager.filter(username= username))> 0:
			messages.append('username is already in use')
		if len(password) < 1:
			messages.append('username is required')
		elif len(password) < 8:
			messages.append('password has to be more that 8 characters')
		if len(comfirmpass) < 1:
			messages.append('conformed paas is required')
		elif password != comfirmpass:
			messages.append('password and confirmed pass must match')
		if now >= start_date :
			messages.append('start date cannot be past date')
		if len(messages) == 0:
			hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			user = User.userManager.create(name=name, username=username, password=hash)

			return (True, user)
		else:
			return (False, messages)

	def login(self, username, password):
		messages =[]
		if len(username) < 1:
			messages.append('name is required')
		if len(password) < 1:
			messages.append('username is required')
		if len(messages) == 0:
			user = User.userManager.filter(username=username)
			if len(user) == 0:
				messages.append('username not found')
				return (False, messages)
			else:
				if bcrypt.checkpw(password.encode(), user[0].password.encode()):
					return (True, user)
				else:
					messages.append('Incorrect password')
					return (False, messages)
		else:
			return (False, messages)

class JointManager(models.Manager):
	def join(self, user_id, wishlist_id):
		this_user = User.userManager.get(id=user_id)
		this_wish = WishList.objects.get(id= wishlist_id)
		joint = Joint.jointManager.create(user=this_user, wishList=this_wish)
		return (joint)

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	userManager = UserManager()
	def __str__(self):
		return self.name + " " + self.username

class WishList(models.Model):
	item = models.CharField(max_length=255)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	def __str__(self):
		return self.item 
class Joint(models.Model):
	user = models.ForeignKey(User)
	wishlist = models.ForeignKey(WishList)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	jointManager = JointManager()
	
	
