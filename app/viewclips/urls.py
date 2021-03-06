from django.views.generic.base import RedirectView
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('about', views.about, name="about"),
	path("upload", views.upload, name="upload"),
	path('directview/<str:vidEpoch>', views.directview, name="directview"),
	path("favicon.ico", RedirectView.as_view(url="/static/media/img/favicon.ico")),
	path("apple-touch-icon.png", RedirectView.as_view(url="/static/media/img/apple-favicon.ico")),
]
