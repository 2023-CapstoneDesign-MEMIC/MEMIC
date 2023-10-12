from pytube import YouTube
import ssl
import numpy
import librosa
import soundfile
import os
import soundfile
from pydub import AudioSegment
import audioread.ffdec
import warnings
import subprocess
from moviepy.editor import *
import sys

sys.path.append('/path/to/ffmpeg')
warnings.filterwarnings('ignore')
ssl._create_default_https_context = ssl._create_unverified_context
AudioSegment.ffmpeg = "/path/to/ffmpeg/bin/ffmpeg"
AudioSegment.ffprobe = "/path/to/ffmpeg/bin/ffprobe"
def trim_audio_data(audio_file,start,end):
    y,sr= librosa.load(audio_file)
    print(y)
    print(sr)
    ny = y[sr*start:sr*end]
    print(ny)
    audio_file = audio_file.replace('.wav', ' new.wav')
    print(audio_file)
    soundfile.write(audio_file,ny,sr,format="wav")
    #librosa.output.write_wav(audio_file, ny, sr)

link = input("Enter\n")
yt=YouTube(link)
filepath=yt.streams.filter(only_audio=True).first().download()
mp4=AudioSegment.from_file(filepath,format="mp4")
wavFilePath = filepath.replace('mp4','wav')
mp4.export(wavFilePath,format='wav')
print('wav convert complete')
print(wavFilePath)
start,end = map(int,input("input start, end time\n").split())
trim_audio_data(wavFilePath,start,end)
# https://www.youtube.com/watch?v=6uCaEDM-Kf8&ab_channel=SlipySlidy # 시간의 신전
# https://www.youtube.com/watch?v=4txU5sWSew3g&ab_channel=PinkSweat%24-Topic # 기타