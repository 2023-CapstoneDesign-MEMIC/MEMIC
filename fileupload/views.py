from django.shortcuts import render, redirect, HttpResponse
from .forms import FileUploadForm
from .models import FileUpload
from pytube import *
import librosa
import soundfile
from pydub import AudioSegment
import os
from django.contrib import messages
from wsgiref.util import FileWrapper


def fileUpload(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        img = request.FILES["imgfile"]
        fileupload = FileUpload(
            title=title,
            content=content,
            imgfile=img,
        )
        fileupload.save()
        return redirect('fileupload')
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)


def youtube(request):
    # checking whether request.method is post or not
    if request.method == 'POST':
        # getting link from frontend
        link = request.POST['link']
        start = request.POST['start']
        end = request.POST['end']
        video = YouTube(link)

        # downloading video -> wav
        audio = video.streams.filter(only_audio=True).first()
        downloaded_file = audio.download()
        base, ext = os.path.splitext(downloaded_file)
        new_file = base + '.wav'
        os.rename(downloaded_file, new_file)

        # cutting audio
        y, sr = librosa.load(new_file)
        start = float(start)
        end = float(end)
        start = int(start * sr)
        end = int(end * sr)
        y = y[start:end]
        soundfile.write(new_file, y, sr)

        # extracting voice and accompaniment
        path = os.path.dirname(new_file)
        file_name = os.path.basename(new_file)
        stems = str(input('stems 선택 : 2, 4, 5 >>> '))

        #stems = '2'

        nsfile_name = file_name.replace(' ', '_')
        try:
            os.rename(new_file, path + '/' + nsfile_name)
            # os.rename(path + file_name, path + nsfile_name)
        except FileNotFoundError:
            pass

        print('기다려주세요.')
        spl = r'spleeter separate -p spleeter:' + \
              str(stems) + r'stems -o output ' + nsfile_name
        os.system(spl)

        # converting wav -> mp3
        # returning HTML page
        return render(request, 'youtube.html')
    return render(request, 'youtube.html')



