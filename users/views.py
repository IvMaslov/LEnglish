from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from lenglish.utils import get_user_info_from_request, get_new_word_from_request, get_current_user, AuthMixin, DataMixin
from random import sample
from .models import Users
from main.models import Words

# Create your views here.

class RegistrationUser(DataMixin, View):

	def get(self, request):
		context_data = self.get_context_data(title="Registration")
		if request.user.is_authenticated:
			return HttpResponseRedirect("/profile/" + request.user.username)

		return render(request, "users/registration.html", context_data)

	def post(self, request):
		#0 - Fine
		#1 - Wrong data
		#2 - User already exists

		email, nickname, password = get_user_info_from_request(request)

		if not email or not nickname or not password:
			return JsonResponse({"status": "1"})


		user = Users.objects.filter(email=email)
		if not user:
			user = Users.objects.create_user(email=email, username=nickname, password=password)
		else:
			return JsonResponse({"status": "2"})

		return JsonResponse({"status": "0"})


class AuthUser(DataMixin, View):

	def get(self, request):
		context_data = self.get_context_data(title="Auth")
		if request.user.is_authenticated:
			return HttpResponseRedirect("/profile/" + request.user.username)


		return render(request, 'users/auth.html', context_data)

	def post(self, request):
		#0 - Fine
		#1 - Wrong data

		email, nickname, password = get_user_info_from_request(request)

		user = authenticate(request, email=email, nickname=nickname, password=password)

		if user:
			login(request, user)

			return JsonResponse({"status": "0", "url":"/"})

		return JsonResponse({"status": "1"})


class LogoutUser(View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect("/auth")


class ProfileUser(AuthMixin, DataMixin, View):
	def get(self, request, nickname):
		context_data = self.get_context_data(title="Not Found")
		user = get_current_user(nickname=nickname)

		if user:
			users_email = self.get_users_email(request)
			if user.username == request.user.username:
				context_data = self.get_context_data(title=user.username)
				user_fields = [user.email, user.username, user.date_joined, user.last_login]

				return render(request, 'users/profile.html', {"user_found": True, "user_fields":user_fields, **users_email, **context_data})

			else:
				return render(request, 'users/profile.html', {"user_found": False, **users_email})
		else:
			return render(request, 'users/profile.html', {"user_found": False})


class DictionaryUser(AuthMixin, DataMixin, View):
	def get(self, request, nickname):
		context_data = self.get_context_data(title="Not Found")
		page = request.GET.get("page")
		user = get_current_user(nickname=nickname)


		if user:
			users_email = self.get_users_email(request)
			if user.username == request.user.username:
				context_data = self.get_context_data(title=request.user.username)
				users_words = user.words.all()
				paginator = Paginator(users_words, 30)

				showing_page = paginator.get_page(page)
				showing_page.object_list = [(i, p) for i,p in enumerate(showing_page.object_list)]


				return render(request, 'users/dictionary.html', {"user_found":True, "paginator":paginator,"page":showing_page, **users_email, **context_data})
			else:
				return render(request, 'users/dictionary.html', {"user_found":False, **users_email})
		else:
			return render(request, 'users/dictionary.html', {"user_found":False})


class QuizUser(AuthMixin, DataMixin, View):
	def get(self, request, nickname):
		user = get_current_user(nickname)

		if user:
			users_email = self.get_users_email(request)
			if user.username == request.user.username:
				context_data = self.get_context_data(title=request.user.username + "'s quiz")


				return render(request, "users/quiz.html", {"user_found": True, **context_data, **users_email})
			else:
				return render(request, "users/quiz.html", {"user_found":False})
		else:
			return render(request, "users/quiz.html", {"user_found":False})

	def post(self, request, nickname):
		user = get_current_user(nickname)

		if user:
			users_email = self.get_users_email(request)
			if user.username == request.user.username:
				reverse = request.GET.get("reverse")
				if not reverse:
					reverse = False

				users_words = user.words.all()

				if len(users_words) < 4:
					return JsonResponse({"user_found":True, "enouth_words":False})
				print(users_words)
				random_4_words = sample(list(users_words), k=4)


				if not reverse:
					random_4_words = [{"word":elem.word, "translate":elem.translate.split(",")[0]} for elem in random_4_words]
				elif reverse:
					random_4_words = [{"word":elem.translate, "translate":elem.word.split(",")[0]} for elem in random_4_words]
				return JsonResponse({"translations": random_4_words, "user_found": True, "enouth_words":True,  **users_email})

			else:
				return JsonResponse({"user_found": False})
		else:
			return JsonResponse({"user_found": False})


class CreateWordUser(View):
	def post(self, request):
		word, translate, level = get_new_word_from_request(request)

		if request.user.is_authenticated:
			word_elem = Words(word=word, translate=translate, user_level=level)
			word_elem.save()

			request.user.words.add(word_elem)

			return JsonResponse({"status":"ok"})
		return JsonResponse({"status":"error"})


class DeleteWordUser(View):
	def post(self, request):
		word, translate, level = get_new_word_from_request(request)
		print(word, translate, level)
		try:
			word_elem = request.user.words.get(word=word, translate=translate, user_level=level)
		except Users.DoesNotExist:
			return JsonResponse({"status":"error"})
		except Words.DoesNotExist:
			return JsonResponse({"status":"error"})

		if request.user.is_authenticated:
			request.user.words.remove(word_elem)

			return JsonResponse({"status":"ok"})
		return JsonResponse({"status":"error"})