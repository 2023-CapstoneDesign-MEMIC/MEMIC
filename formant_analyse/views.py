from django.shortcuts import render

#using librosa, extract mfcc from audio file "voice.wav"
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn
import parselmouth
from sklearn import metrics
from scipy.signal import find_peaks


def FormantAnalys(request):
    y1, sr1 = librosa.load('sourceVocal.wav')
    y2, sr2 = librosa.load('userVocal.wav')

    # 'sourceVocal.wav'의 frequency, amplitude 출력 코드
    n_fft = 512
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
    plt.savefig('sourceVocalPicked.png')

    # FIXME : amplitude 값이 예측과는 다르게 나옴. 대체재로 praat 구현 시도하는 중
    # # 'userVocal.wav'의 frequency, amplitude 출력 코드
    # n_fft = 512
    # plt.figure(figsize=(12, 4))
    # ft2 = np.abs(librosa.stft(y2[:n_fft], hop_length=n_fft + 1))
    # ft2 = ft2.flatten()
    # plt.plot(ft2)
    # plt.title('Spectrum')
    # plt.xlabel('Frequency Bin')
    # plt.ylabel('Amplitude')
    # plt.show()
    #
    # # peak picking
    # peaks1, _ = find_peaks(ft2, height=0.1)
    # plt.figure(figsize=(10, 4))
    # plt.plot(ft2, alpha=0.5, label='userVocal')
    # plt.plot(peaks1, ft2[peaks1], "x")
    # plt.legend()
    # plt.show()
    # plt.savefig('userVocalPicked.png')

    # 아래부터는 praat를 이용한 시간(time_step) 별 formant 계산 코드임.
    data1 = pd.DataFrame({
        "times": [],
        "F0(pitch)": [],
        "F1": [],
        "F2": [],
        'F3': [],
        "F4": [],
        "F5": [],
        "filename": []
    })

    data2 = pd.DataFrame({
        "times": [],
        "F0(pitch)": [],
        "F1": [],
        "F2": [],
        'F3': [],
        "F4": [],
        "F5": [],
        "filename": []
    })

    # 'sourceVocal.wav'의 parselmouth.Sound 객체 생성 코드
    sound1 = parselmouth.Sound("sourceVocal.wav")
    sound2 = parselmouth.Sound("userVocal.wav")

    # 'sourceVocal.wav'의 formant 출력 코드
    formant1 = sound1.to_formant_burg(time_step=0.1)

    # 'userVocal.wav'의 formant 출력 코드
    formant2 = sound2.to_formant_burg(time_step=0.1)

    # Pitch
    pitch1 = sound1.to_pitch()
    pitch2 = sound2.to_pitch()
    df1 = pd.DataFrame({"times": formant1.ts()})
    df2 = pd.DataFrame({"times": formant2.ts()})

    # F1~F5까지 계산
    for idx, col in enumerate(["F1", "F2", "F3", "F4", "F5"], 1):
        df1[col] = df1['times'].map(lambda x: formant1.get_value_at_time(formant_number=idx, time=x))
        df2[col] = df2['times'].map(lambda x: formant1.get_value_at_time(formant_number=idx, time=x))

    df1['F0(pitch)'] = df1['times'].map(lambda x: pitch1.get_value_at_time(time = x))
    df1['filename'] = "sourceVocal.wav"
    df2['F0(pitch)'] = df2['times'].map(lambda x: pitch2.get_value_at_time(time = x))
    df2['filename'] = "userVocal.wav"
    data1 = data1.append(df1)
    data2 = data2.append(df2)

    print(data1)
    print(data2)
    print(formant1, formant2)

    # TODO : 위에서 얻어낸 시간별 포먼트 비교
    # TODO : 큰 차이가 난다고 판단하는 기준과 구간 별 피드백 문장 구현

    return render(request, 'formant_analyse.html')


def FormantAnalysPraat(request):
    sound1 = parselmouth.Sound("sourceVocal.wav")
    sound2 = parselmouth.Sound("userVocal.wav")

    # 'sourceVocal.wav'의 formant 출력 코드
    formant1 = sound1.to_formant_burg(time_step=0.1)

    # 'userVocal.wav'의 formant 출력 코드
    formant2 = sound2.to_formant_burg(time_step=0.1)

    # formant 값을 그래프로 출력
    plt.figure()
    plt.plot(formant1.xs(), formant1.values.T[0, :], 'o', label="F1")
    plt.plot(formant1.xs(), formant1.values.T[1, :], 'o', label="F2")
    plt.plot(formant1.xs(), formant1.values.T[2, :], 'o', label="F3")
    plt.legend()
    plt.grid(True)
    plt.xlabel("time [s]")
    plt.ylabel("Formant Frequencies [Hz]")
    plt.show()

    # formant 값을 그래프로 출력
    plt.figure()
    plt.plot(formant2.xs(), formant2.values.T[0, :], 'o', label="F1")
    plt.plot(formant2.xs(), formant2.values.T[1, :], 'o', label="F2")
    plt.plot(formant2.xs(), formant2.values.T[2, :], 'o', label="F3")
    plt.legend()
    plt.grid(True)
    plt.xlabel("time [s]")
    plt.ylabel("Formant Frequencies [Hz]")
    plt.show()


    # Pitch값
    pitch1 = sound1.to_pitch()
    pitch2 = sound2.to_pitch()

    # Pitch값을 그래프로 출력
    plt.figure()
    plt.plot(pitch1.xs(), pitch1.selected_array['frequency'])
    plt.grid(True)
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")
    plt.xlim([0, sound1.xmax])
    plt.show()

    print(formant1, formant2)
