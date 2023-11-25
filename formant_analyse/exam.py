from django.shortcuts import render

import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
from fastdtw import fastdtw
import pandas as pd
import numpy as np
import parselmouth
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity

# row 생략 없이 출력
pd.set_option('display.max_rows', None)
# col 생략 없이 출력
pd.set_option('display.max_columns', None)

def compute_mfcc(yk, srk):
    mfcc = librosa.feature.mfcc(y=yk, sr=srk)
    return mfcc.T

def compute_similarity(y1, sr1, y2, sr2):
    mfcc1 = compute_mfcc(y1, sr1)
    mfcc2 = compute_mfcc(y2, sr2)

    # y1, y2(time sequence)에 대한 enumrated index의 mfcc값 DTW, 즉 dtwSeq는 (y1, y2)로 이루어진 배열
    dtwDist, dtwSeq = fastdtw(mfcc1, mfcc2)

    # #print(dtwSeq)
    # for d in dtwSeq:
    #     print(d)
    #     print(sr1*d[0] + sr1 )
    #     print(mfcc1[d[0]], mfcc2[d[1]])

    combined_similarity_percent = 0
    return dtwDist, dtwSeq, combined_similarity_percent

audio_file1 = 'sourceVocal.wav'
audio_file2 = 'userVocal.wav'

#sound1 = parselmouth.Sound(audio_file1)
sound1 = parselmouth.Sound(audio_file1)
sound2 = parselmouth.Sound(audio_file2)

y1, sr1 = librosa.load(audio_file1)
y2, sr2 = librosa.load(audio_file2)

distance, path, similarity_ALL = compute_similarity(y1, sr1, y2, sr2)

formant_array1 = []
formant_array2 = []

data1 = pd.DataFrame({
    "times": [],
    "OG times": [],
    "F0(pitch)": [],
    "F1": [],
    "F2": [],
    'F3': [],
    "filename": []
})

data2 = pd.DataFrame({
    "times": [],
    "OG times": [],
    "F0(pitch)": [],
    "F1": [],
    "F2": [],
    'F3': [],
    "filename": []
})

for mapped in path:
    # DTW 결과에서 가져온 idx1 : sourceVocal.wav의 인덱스, idx2 : userVocal.wav의 인덱스
    idx1, idx2 = mapped

    # 해당 인덱스에 대한 실제 시간.
    time_audio1 = librosa.frames_to_time(idx1, sr=sr1)
    time_audio2 = librosa.frames_to_time(idx2, sr=sr2)

    # 그 시간에서 0.1초만큼 컷팅
    mapped_sound1 = sound1.extract_part(from_time=time_audio1, to_time=time_audio1+0.1)
    mapped_sound2 = sound2.extract_part(from_time=time_audio2, to_time=time_audio2+0.1)

    # 0.1초만큼 컷팅한 부분 Formant 추출 -> 0.1초 한 구간의 평균값만 나옴.
    formant1 = mapped_sound1.to_formant_burg(time_step=0.1)
    formant2 = mapped_sound2.to_formant_burg(time_step=0.1)

    # pitch 추출
    pitch1 = mapped_sound1.to_pitch()
    pitch2 = mapped_sound2.to_pitch()

    df1 = pd.DataFrame({"times": formant1.ts()})
    df2 = pd.DataFrame({"times": formant2.ts()})

    #print(f"Audio 1 Time: {time_audio1}, Audio 2 Time: {time_audio2}")
    df1['OG times'] = time_audio1
    df2['OG times'] = time_audio2
    # F1~F3까지 계산
    for idx, col in enumerate(["F1", "F2", "F3"], 1):
        df1[col] = df1['times'].map(lambda x: formant1.get_value_at_time(formant_number=idx, time=x))
        df2[col] = df2['times'].map(lambda x: formant1.get_value_at_time(formant_number=idx, time=x))

    df1['F0(pitch)'] = df1['times'].map(lambda x: pitch1.get_value_at_time(time=x))
    df1['filename'] = "sourceVocal.wav"
    df2['F0(pitch)'] = df2['times'].map(lambda x: pitch2.get_value_at_time(time=x))
    df2['filename'] = "userVocal.wav"

    # data1 = data1.append(df1)
    # data2 = data2.append(df2)

    data1 = pd.concat([data1, df1])
    data2 = pd.concat([data2, df2])

    #print(formant1, formant2)
    #print(formant1.ts())
    #print(formant1.get_value_at_time(formant_number="F1", time=0.1))
    # formant_array1.append(formant1)
    # formant_array2.append(formant2)

#
print(data1)
print(data2)