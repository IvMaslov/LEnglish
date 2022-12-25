from users.models import Users
import json

def get_user_info_from_request(request):
	json_data = json.loads(request.body.decode("utf-8"))
	email = json_data.get("email")
	nickname = json_data.get("nickname")
	password = json_data.get("password")

	return email, nickname, password

def get_new_word_from_request(request):
	json_data = json.loads(request.body.decode("utf-8"))
	word = json_data.get("word")
	translate = json_data.get("translate")
	level = json_data.get("level")

	return word, translate, level


def get_current_user(nickname=None, email=None):
	if nickname:
		try:
			user = Users.objects.get(username=nickname)
		except Users.DoesNotExist:
			user = None
		return user
	elif email:
		try:
			user = Users.objects.get(email=email)
		except Users.DoesNotExist:
			user = None
		return user
	else:
		return None


class AuthMixin:

	def get_users_email(self, request):
		if request.user.is_authenticated:
			users_email = request.user.email
		else:
			users_email = None

		return {
			"authenticated": request.user.is_authenticated,
			"users_email": users_email,
			"user_url":"/profile/{}".format(request.user.username),
			"dictionary_url":"/dictionary/{}".format(request.user.username),
			"quiz_url":"/quiz/{}".format(request.user.username)
		}


class DataMixin:

	def get_context_data(self, **kwargs):
		return kwargs