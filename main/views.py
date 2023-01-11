from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from random import sample
from .models import Words, Levels
from lenglish.utils import get_user_info_from_request, AuthMixin, DataMixin
# Create your views here.

class IndexView(AuthMixin, DataMixin, View):
	def get(self, request):
		levels = Levels.objects.all()
		users_email = self.get_users_email(request)
		context_data = self.get_context_data(title="Words")

		return render(request, "main/index.html", dict(list(context_data.items()) + list(users_email.items())))

def pageNotFound(request, exception):
	return HttpResponseNotFound("Sorry for this, we are haven't this page")

class LevelView(AuthMixin, DataMixin, View):
	def get(self, request, slug_id):
		users_email = self.get_users_email(request)
		context_data = self.get_context_data(title="Levels")

		return render(request, "main/levels.html", dict(list(context_data.items()) + list(users_email.items())))

	def post(self, request, slug_id):
		reverse = request.GET.get("reverse")
		if not reverse:
			reverse = False

		obj = get_object_or_404(Levels, slug=slug_id)

		words = Words.objects.filter(word_category=obj.id)
		random_4_words = sample(list(words), k=4)

		if not reverse:
			random_4_words = [{"word":elem.word, "translate":elem.translate.split(",")[0]} for elem in random_4_words]
		elif reverse:
			random_4_words = [{"word":elem.translate, "translate":elem.word.split(",")[0]} for elem in random_4_words]
		return JsonResponse({"translations": random_4_words})

