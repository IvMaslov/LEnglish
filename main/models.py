from django.db import models
from django.urls import reverse

# Create your models here.

class Words(models.Model):
	word = models.CharField(max_length=70)
	translate  = models.CharField(max_length=70)
	user_level = models.CharField(max_length=10, null=True)
	word_category = models.ForeignKey("Levels", on_delete=models.CASCADE, null=True)

	def __repr__(self):
		return "Word with name: <{word}>".format(word = self.word)

class Levels(models.Model):
	level = models.CharField(max_length=100, db_index=True)
	slug = models.SlugField(max_length=100, unique=True, db_index=True)

	def __repr__(self):
		return "Levels with name <{name}>".format(name=self.level)

	def get_absolute_url(self):
		return reverse("level", kwargs={"slug_id": self.slug})
