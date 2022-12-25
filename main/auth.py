from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password, make_password
from users.models import Users


class CustomAuthenticateBackend(BaseBackend):
	def get_user(self, user_id):
		try:
			return Users.objects.get(pk=user_id)
		except Users.DoesNotExist:
			return None


	def authenticate(self, request, email=None, nickname=None, password=None):
		if email:
			try:
				user = Users.objects.get(email=email)
			except Users.DoesNotExist:
				return None
		elif nickname:
			try:
				user = Users.objects.get(username=nickname)
			except Users.DoesNotExist:
				return None
		else:
			return None

		password_verify = user.check_password(password)

		if password_verify:
			return user
		return None
