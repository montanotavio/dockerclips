from django.views.generic.base import RedirectView
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('about', views.about, name="about"),
	path("upload", views.upload, name="upload"),
	path("favicon.ico", RedirectView.as_view(url="/static/media/favicon.ico")),
	path("apple-touch-icon.png", RedirectView.as_view(url="/static/media/apple-favicon.ico")),
]
