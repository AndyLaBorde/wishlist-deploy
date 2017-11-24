from __future__ import unicode_literals

from django.db import models

import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):

	def register(self, form_data):
		pw = str(form_data['password'])
		h_pw = bcrypt.hashpw(pw, bcrypt.gensalt())

		user = User.objects.create(
			name = form_data['name'],
			username = form_data['username'],
			email = form_data['email'],
			password = h_pw,
			datehired = form_data['date']
			)
		return user


	def register_validation(self, form_data):
		errors = []

		if len(form_data['name']) < 3:
			errors.append('Name is required.')
		if len(form_data['username']) < 3:
			errors.append('Username is Required.')
		if len(form_data['email']) == 0 or not EMAIL_REGEX.match(form_data['email']):
			errors.append('Invalid Email.')
		if len(form_data['password']) < 8:
			errors.append('A Password must contain more than 8 characters.')
		if form_data['password'] != form_data['confirmpw']:
			errors.append('Passwords do not match!')
		duplicate = User.objects.filter(email = form_data['email'])
		if len(duplicate) == 1:
			errors.append('Email already exists')
		if form_data['date'] == None:
			errors.append('Must enter a Hired Date!')

		return errors

	def login(self, form_data):
		user = User.objects.all().filter(username= form_data['username'])[0]
		return user

	def login_validation(self, form_data):
		errors = []
		user = User.objects.filter(username= form_data['username']).first()
		if user:
			pw = str(form_data['password'])
			user_password = str(user.password)
			pw_check = bcrypt.hashpw(pw.encode(), user_password.encode())
			if not user_password == pw_check:
				errors.append('Invalid Password')
		else: 
			errors.append('Invalid Username')

		return errors



class User(models.Model):
	name = models.CharField(max_length = 45)
	username = models.CharField(max_length = 45)
	email = models.CharField(max_length = 45)
	password = models.CharField(max_length = 45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	datehired = models.DateField()
	

	def __unicode__(self):
		return 'id :' + str(self.id) + ', name :' + self.name + ', username :' + self.username + ', email:' + self.email + ', password :' + self.password + ', datehired :' + str(self.datehired)

# class Item(models.Model):
#     title=models.CharField(max_length=64)
#     user=models.ForeignKey(Users, related_name='items')
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __unicode__(self):
#     	return 'id :' + str(self.id) + ', title :' + self.title
class WishManager(models.Manager):
	def create_wish_validations(self, form_data):
		errors = []

		if len(form_data['item']) < 1:
			errors.append("Item must not be blank") 

		return errors
	def addItem(self, form_data, user_id):
		item = Wish.objects.create(
			wish = form_data['item'],
			created_by = User.objects.get(id = user_id)
			)
		print item


class Wish(models.Model):

    wish=models.CharField(max_length= 45)
    added_by = models.ManyToManyField(User, related_name='wishes')
    created_by=models.ForeignKey(User, related_name='added_items')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = WishManager()

    def __unicode__(self):
    	return 'id :' + str(self.id) + ', wish :' + self.wish + ', added_by :' + str(self.added_by) + ', created_by :' + str(self.created_by)
