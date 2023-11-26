from django.urls import path
from .views import *

urlpatterns = [
	path('record/', AudioFileCreateViewMixin.as_view(), name="audio_recorder"),
]