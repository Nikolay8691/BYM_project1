from django.db import models
from datetime import date, datetime

from django.contrib.auth.models import User

# Create your models here.
class Profile_admin(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	nick = models.CharField(max_length = 32)
	phone = models.CharField(max_length = 32, blank = True)

	f_name = models.CharField(max_length = 64)
	l_name = models.CharField(max_length = 64)
	email = models.EmailField(default = 'admin@ya.ru')
	
	def __str__(self):
		return f' admin_name : {self.user.username} ({self.nick} - email : {self.email})'

class Profile_user(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	
	f_name = models.CharField(max_length = 64)
	l_name = models.CharField(max_length = 64)

	email = models.EmailField(blank = True)
	phone = models.CharField(max_length = 32, blank = True)

	age = models.IntegerField(default = 1, blank = True)
	sex = models.CharField(max_length = 7, blank = True)
	birthday = models.DateField(default = date.today, blank = True)

	def __str__(self):
		return f' login_name : {self.user.username} ({self.f_name} {self.l_name})'
