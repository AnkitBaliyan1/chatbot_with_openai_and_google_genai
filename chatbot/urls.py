from django.urls import path
from . import views


app_name = "chatbot"
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.home, name='home'),
    path('about/', views.about, name="about"),
    path('openai-bot/', views.openai_bot, name="openai"),
    path('gemini-bot/', views.gemini_bot, name="gemini"),
    path('input/',views.input_view, name='input'),
]


