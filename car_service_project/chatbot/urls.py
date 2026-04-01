# chatbot/urls.py
from django.urls import path
from .views import chatbot_response
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat-api/', chatbot_response, name='chatbot_response'),
]
