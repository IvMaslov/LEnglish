from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import Words

# Create your models here.
class Users(AbstractUser):
	words = models.ManyToManyField(Words)

	def __repr__(self):
		return "User with name {}".format(self.username)