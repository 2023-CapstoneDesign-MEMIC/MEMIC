from django import http
from django.views.generic.base import View
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views import View
import os
class indexView(View):
    def get(self, request):
        return render(request, 'record.html')
class AudioFileCreateViewMixin(View):
    model = None
    create_field = None

    def create_object(self, audio_file):
        return self.model.objects.create(**{self.create_field: audio_file})

    # def post(self, request):
    #     audio_file = request.FILES.get('audio_file', None)
    #     print("asdasd")
    #     print(audio_file)
    #     if audio_file is None:
    #         return http.HttpResponseBadRequest()
    #     result = self.create_object(audio_file)
    #     print(result.audio_file.url)
    #     return http.JsonResponse({
    #         'id': result.pk,
    #         'url': result.audio_file.url,
    #     }, status=201)

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('audio_file', None)
        if audio_file is None:
            return JsonResponse({'error': 'No audio file provided'}, status=400)

        # 여기서 파일을 저장하거나 다른 처리를 수행합니다.
        # 예를 들어, 저장된 파일의 경로를 사용하여 응답을 생성할 수 있습니다.
        #file_path = '/path/to/uploaded/file'  # 여기에 실제 파일 경로를 넣어주세요.
        current_directory = os.path.dirname(os.path.abspath(__file__))
        processed_file_path = os.path.join(current_directory, 'record_audio.wav')

        print()
        print("asdasdasdfasfnasfaiosdfnjaoijfo")
        print()
        print(processed_file_path)
        print()
        print()
        return JsonResponse({'file_path': processed_file_path}, status=201)