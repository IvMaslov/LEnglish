from django.urls import path
from . import views

urlpatterns = [
	path("registration", views.RegistrationUser.as_view(), name="registration"),
	path("auth", views.AuthUser.as_view(), name="auth"),
	path("logout", views.LogoutUser.as_view(), name="logout"),
	path("profile/<str:nickname>", views.ProfileUser.as_view(), name="profile"),
	path("dictionary/<str:nickname>", views.DictionaryUser.as_view(), name="dictionary"),
	path("quiz/<str:nickname>", views.QuizUser.as_view(), name="quiz"),
	path("create/word", views.CreateWordUser.as_view(), name="create_word"),
	path("delete/word", views.DeleteWordUser.as_view(), name="delete_word")
]