from django.urls import path
from . import views

urlpatterns = [
	path("", views.IndexView.as_view(), name="index"),
	path("level/<slug:slug_id>", views.LevelView.as_view(), name="level"),
]