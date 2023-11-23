from django.urls import path
from .views import *

urlpatterns = [
	path('fileupload/', fileUpload, name="fileupload"),
	path('fileupload/youtube', youtube, name="youtube"),
	#path('fileupload/fileUpload', fileUpload, name="fileUpload"),
]