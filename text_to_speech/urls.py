from django.urls import path
from . import views

urlpatterns = [
    path('tts/', views.text_to_speech, name='text_to_speech'),
    path('stt/', views.speech_to_text, name='speech_to_text'),
]
