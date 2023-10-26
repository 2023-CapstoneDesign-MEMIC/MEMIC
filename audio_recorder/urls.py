from django.urls import path
from .views import *

urlpatterns = [
	path('record/', indexView.as_view(), name="audio_recorder"),
]