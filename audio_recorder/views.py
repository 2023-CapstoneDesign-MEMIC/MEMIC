from django import http
from django.views.generic.base import View
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views import View
import os
import boto3
import soundfile
from io import BytesIO
from pydub import AudioSegment
from botocore.exceptions import NoCredentialsError

AudioSegment.ffmpeg ='/opt/homebrew/bin/ffmpeg'
class indexView(View):
    def get(self, request):
        return render(request, 'record.html')
class AudioFileCreateViewMixin(View):
    model = None
    create_field = None

    def create_object(self, audio_file):
        return self.model.objects.create(**{self.create_field: audio_file})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            audio_file = request.FILES.get('audio_file', None)

            # Your S3 configuration
            access_key = ''
            secret_key = ''
            bucket_name = 'memicbucket'
            s3_file_path = 'RecordingFile/' + audio_file.name

            # Upload file to S3
            s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            s3.upload_fileobj(BytesIO(audio_file.read()), bucket_name, s3_file_path)

            return JsonResponse({'message': 'Upload Successful', 's3_file_path': s3_file_path})

        return JsonResponse({'error': 'Invalid request method'}, status=400)