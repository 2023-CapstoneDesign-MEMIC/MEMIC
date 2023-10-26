from django.shortcuts import render

#using librosa, extract mfcc from audio file "voice.wav"
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn
from sklearn import metrics
from scipy.signal import find_peaks


def FormantAnalys(request):
    # # 'voice.wav' 와 'accompaniment.wav' 의 포먼트 좌표 배열 생성 코드
    # # voice.wav의 포먼트 좌표 배열 생성 코드
    # y1, sr1 = librosa.load('sourceVocal.wav')
    # pitches1, magnitudes1 = librosa.piptrack(y=y1, sr=sr1)
    # pitches1 = pitches1.T
    # #pitches1 = pitches1[0]
    #
    # # accompaniment.wav의 포먼트 좌표 배열 생성 코드
    # y2, sr2 = librosa.load('userVocal.wav')
    # pitches2, magnitudes2 = librosa.piptrack(y=y2, sr=sr2)
    # pitches2 = pitches2.T
    # #pitches2 = pitches2[0]
    #
    # # 'voice.wav' 와 'accompaniment.wav' 의 포먼트 좌표 배열을 csv 파일로 저장
    # pitches1_df = pd.DataFrame(pitches1)
    # pitches1_df.to_csv('pitches1.csv', index=False)
    # pitches2_df = pd.DataFrame(pitches2)
    # pitches2_df.to_csv('pitches2.csv', index=False)
    #
    # # 두 포먼트 좌표 배열을 시각화
    # plt.figure(figsize=(10, 10))
    # plt.plot(pitches1, label='sourceVocal')
    # plt.plot(pitches2, label='userVocal')
    # plt.legend()
    # plt.show()
    #
    # # 두 포먼트 좌표 배열을 출력
    # print(y1, y2)
    # print(pitches1)
    # print(pitches2)

    # 'sourceVocal.wav' 와 'userVocal.wav' 의 mel spectrogram 생성 및 출력 코드
    # sourceVocal.wav의 mel spectrogram 생성 및 출력 코드
    y1, sr1 = librosa.load('sourceVocal.wav')
    S1 = librosa.feature.melspectrogram(y=y1, sr=sr1)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.power_to_db(S1, ref=np.max), y_axis='mel', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    plt.show()

    # userVocal.wav의 mel spectrogram 생성 및 출력 코드
    y2, sr2 = librosa.load('userVocal.wav')
    S2 = librosa.feature.melspectrogram(y=y2, sr=sr2)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.power_to_db(S2, ref=np.max), y_axis='mel', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    plt.show()

    # 'sourceVocal.wav'의 frequency, amplitude 출력 코드
    n_fft = 2048
    plt.figure(figsize=(12, 4))
    ft = np.abs(librosa.stft(y1[:n_fft], hop_length=n_fft + 1))
    ft = ft.flatten()
    plt.plot(ft)
    plt.title('Spectrum')
    plt.xlabel('Frequency Bin')
    plt.ylabel('Amplitude')
    plt.show()

    # peak picking
    peaks1, _ = find_peaks(ft, height=0.1)
    plt.figure(figsize=(10, 4))
    plt.plot(ft, alpha=0.5, label='sourceVocal')
    plt.plot(peaks1, ft[peaks1], "x")
    plt.legend()
    plt.show()

    # 'userVocal.wav'의 frequency, amplitude 출력 코드
    n_fft = 2048
    plt.figure(figsize=(12, 4))
    ft2 = np.abs(librosa.stft(y2[:n_fft], hop_length=n_fft + 1))
    ft2 = ft2.flatten()
    plt.plot(ft2)
    plt.title('Spectrum')
    plt.xlabel('Frequency Bin')
    plt.ylabel('Amplitude')
    plt.show()

    # peak picking
    peaks1, _ = find_peaks(ft2, height=0.1)
    plt.figure(figsize=(10, 4))
    plt.plot(ft2, alpha=0.5, label='userVocal')
    plt.plot(peaks1, ft2[peaks1], "x")
    plt.legend()
    plt.show()

    return render(request, 'formant_analyse.html')
