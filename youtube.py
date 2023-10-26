from pytube import YouTube
import ssl
import librosa
import soundfile
from pydub import AudioSegment
import warnings
import sys
import os
import numpy
import datetime
import wave

sys.path.append('/path/to/ffmpeg')
warnings.filterwarnings('ignore')
ssl._create_default_https_context = ssl._create_unverified_context
AudioSegment.ffmpeg = "/path/to/ffmpeg/bin/ffmpeg"
AudioSegment.ffprobe = "/path/to/ffmpeg/bin/ffprobe"

# class wav_spleeter():
#     def __init__(self, path):
#         self.path = path
#         self.spl_path = path+"\\spleeter_out\\"
#         self.filelist = [wav for wav in os.listdir(path) if wav.endswith(".wav")]
#         self.filenum = len(self.filelist)
#         self.partnum = list(set(int(i.split('_')[0]) for i in self.filelist))
#         self.filelist = sorted(self.filelist, key=lambda x: int(x.split('_')[0]))
#         self.partnum.sort()
#         self.total_time = 0
#
#         os.chdir(self.path)
#
#         for i in self.filelist:
#             a = wave.open(i, 'rb')
#             self.total_time += a.getnframes() / a.getframerate()
#
#         print(self.partnum)
#         print(self.filelist)
#         print(f'파일이 {self.filenum}개 있습니다.')
#         print(self.total_time)
#         print(f'total time : {datetime.timedelta(seconds=self.total_time)}')
#
#
#
#     """
#     start = 0이면 path안의 모든 wav파일을 spleeter
#     start = n이면 n으로 시작하는 wav파일을 spleeter
#     start와 end값이 둘 다 입력되면 start~end까지의 wav파일을 spleeter
#     """
#
#     def spleeter(self, start, end=0):
#         spl_command = 'spleeter separate -p spleeter:2stems -o spleeter_out '
#         if start==0:
#             for i in self.filelist:
#                 os.system(spl_command+i)
#             print("Done")
#         elif end==0 and (start in self.partnum):
#             for i in self.filelist:
#                 if int(i[0])==start:
#                     os.system(spl_command+i)
#             print("Done")
#         elif start!=0 and end!=0:
#             if start not in self.partnum or end not in self.partnum:
#                 print("RangeError!1")
#             if start>end:
#                 print("end must large then start!")
#             for i in self.filelist:
#                 if i[0]>=start and i[0]<=end:
#                     os.system(spl_command+i)
#             print("Done")
#         else:
#             print("RangeError!2")
#
#
#     """
#     실행 하면 spleeter함수 실행 후 나온 파일들 중 vocal파일을
#     spleeter_out 디렉토리에 배치한다. 그 후 mr파일과 디렉토리는 삭제
#     """
#
#     def spldata_to_path(self):
#         if not (os.path.exists(self.spl_path)):
#             print("plz execute spleeter def!")
#             return 0
#         os.chdir(self.spl_path)
#         spl_dir = [i for i in os.listdir(os.getcwd()) if os.path.isdir(i)]
#         print(spl_dir)
#         if len(spl_dir)==0:
#             print("spleeter 먼저 실행해 주세요. ")
#         for l in spl_dir:
#             try:
#                 os.rename(self.spl_path + l + "\\vocals.wav", self.spl_path + l + "_spl.wav")
#             except FileNotFoundError:
#                 print(l+"폴더에 vocals.wav 파일이 없습니다.")
#             except FileExistsError:
#                 os.remove(self.spl_path + l + "_spl.wav")
#                 os.rename(self.spl_path + l + "\\vocals.wav", self.spl_path + l + "_spl.wav")
#
#         for l in spl_dir:
#             try:
#                 os.remove(self.spl_path + l + "\\accompaniment.wav")
#                 os.rmdir(self.spl_path + l)
#             except FileNotFoundError:
#                 pass
# 	# 폴더 정보를 info.txt에 저장
#     def folderinfo(self):
#         info = os.popen('dir | sort').read()
#         f = open("info.txt", 'w')
#         print(info)
#         f.write(f'wav file total time : {datetime.timedelta(seconds=self.total_time)}\n\n')
#         f.write(f'file_num = {self.filenum}\n\n')
#         f.write(info)
#         f.close()
#
#
# if __name__ == '__main__':
#     path = 'your dataset path'
#     wavfile = wav_spleeter(path)
#     wavfile.folderinfo()
#     wavfile.spleeter(0)
#     wavfile.spldata_to_path()

def trim_audio_data(audio_file,start,end):
    y,sr= librosa.load(audio_file)
    print(y)
    print(sr)
    ny = y[sr*start:sr*end]
    print(ny)
    audio_file = audio_file.replace('.wav', ' new.wav')
    print(audio_file)
    soundfile.write(audio_file,ny,sr,format="wav")
    path = os.path.dirname(audio_file)
    file_name = os.path.basename(audio_file)
    # 2stems = vocals and accompaniment
    # 4stems = vocals, drums, bass, and other
    # 5stems = vocals, drums, bass, piano, and other
    #stems = str(input('stems 선택 : 2, 4, 5 >>>'))
    stems = '2'
    #file_name = str(input('음악 파일의 이름을 적어주세요. >>>'))
    nsfile_name = file_name.replace(' ', '_')

    try:
        os.rename(audio_file, path + '/'+nsfile_name)
        #os.rename(path + file_name, path + nsfile_name)
    except FileNotFoundError:
        pass

    print('기다려주세요.')
    spl = r'spleeter separate -p spleeter:' + \
          str(stems) + r'stems -o output ' + nsfile_name
    #'spleeter separate -p spleeter:2stems -o spleeter_out '
    # spl = r'python -m spleeter separate -p spleeter:' + \
    #       str(stems) + r'stems -o output ' + nsfile_name + '.wav'
    # 'spleeter separate -p spleeter:2stems -o output my_song.mp3'
    os.system(spl)


link = input("Enter\n")
yt=YouTube(link)
filepath=yt.streams.filter(only_audio=True).first().download()
path = os.path.dirname(filepath)
mp4=AudioSegment.from_file(filepath,format="mp4")
wavFilePath = filepath.replace('mp4','wav')
mp4.export(wavFilePath,format='wav')
print('wav convert complete')
print(wavFilePath)
start,end = map(int,input("input start, end time\n").split())
trim_audio_data(wavFilePath,start,end)
# https://www.youtube.com/watch?v=6uCaEDM-Kf8&ab_channel=SlipySlidy # 시간의 신전
# https://www.youtube.com/watch?v=4txU5sWSew3g&ab_channel=PinkSweat%24-Topic # 기타
# https://www.youtube.com/watch?v=cSAU8iUSFWI&ab_channel=%EC%82%AC%EC%9A%B0%EC%8A%A4%EC%BD%94%EB%A6%AC%EC%95%88%ED%8C%8C%ED%81%ACSouthKoreanPark
# 29 32