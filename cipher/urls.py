from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('generate_key', views.generate_key, name='generate_key'),
	path('cipher_message', views.cipher_message, name='cipher_message'),
	path('more-detail', views.more_detail, name='more_detail'),
]
