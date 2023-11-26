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

# def compute_mfcc(yk, srk):
#     mfcc = librosa.feature.mfcc(y=yk, sr=srk)
#     return mfcc.T

def compute_similarity(y1, sr1, y2, sr2):
    mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1)
    mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2)

    mfcc1 = mfcc1.T
    mfcc2 = mfcc2.T

    # y1, y2(time sequence)에 대한 enumrated index의 mfcc값 DTW, 즉 dtwSeq는 (y1, y2)로 이루어진 배열
    dtwDist, dtwSeq = fastdtw(mfcc1, mfcc2)

    cosine_sim = cosine_similarity(mfcc1, mfcc2)

    # 유클리드 거리 계산
    euclidean_dist = np.linalg.norm(mfcc1 - mfcc2)

    # DTW 거리를 비교 데이터 길이에 따라 정규화하여 백분율로 표시
    max_length = max(len(mfcc1), len(mfcc2))
    # 미사용
    normalized_dtw_distance = (1 - dtwDist / max_length) * 100

    # 코사인 유사도를 백분율로 표시
    cosine_similarity_percent = np.mean(cosine_sim) * 100

    # 유클리드 거리를 최대 길이에 대한 비율로 정규화하여 백분율로 표시
    max_euclidean_dist = max_length * max_length
    normalized_euclidean_distance = (1 - euclidean_dist / max_euclidean_dist) * 100

    # 유클리드 거리와 코사인 유사도를 가중 평균하여 종합적인 유사성을 백분율로 표시
    alpha = 0.5  # 가중치 (0에서 1 사이의 값)
    combined_similarity_percent = (alpha * normalized_euclidean_distance + (1 - alpha) * cosine_similarity_percent)

    return dtwDist, dtwSeq, combined_similarity_percent

audio_file1 = 'sourceVocal.wav'
audio_file2 = 'userVocal.wav'

sound1 = parselmouth.Sound(audio_file1)
sound2 = parselmouth.Sound(audio_file2)

y1, sr1 = librosa.load(audio_file1)
y2, sr2 = librosa.load(audio_file2)

distance, path, similarity_ALL = compute_similarity(y1, sr1, y2, sr2)

formant_array1 = []
formant_array2 = []

print("ALL SCORE: ", similarity_ALL)

data = pd.DataFrame({
    "times": [],
    "sTimes": [],
    "uTimes": [],
    "sF0": [],
    "sF1": [],
    "sF2": [],
    'sF3': [],
    "uF0": [],
    "uF1": [],
    "uF2": [],
    'uF3': [],
    'score': []
})

idxnum = 0

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

    mapped_y1, mapped_sr1 = librosa.load(audio_file1, offset=time_audio1, duration=0.1)
    mapped_y2, mapped_sr2 = librosa.load(audio_file2, offset=time_audio2, duration=0.1)

    _d1, _d2, mapped_score = compute_similarity(mapped_y1, mapped_sr1, mapped_y2, mapped_sr2)

    # pitch 추출
    pitch1 = mapped_sound1.to_pitch()
    pitch2 = mapped_sound2.to_pitch()

    df = pd.DataFrame({"times": formant1.ts()}, index=[idxnum])
    idxnum+=1
    df["sTimes"] = time_audio1
    df["uTimes"] = time_audio2

    df['sF0'] = df['times'].map(lambda x: pitch1.get_value_at_time(time=x))
    df['uF0'] = df['times'].map(lambda x: pitch2.get_value_at_time(time=x))

    for idx, col in enumerate(["sF1", "sF2", "sF3"], 1):
        df[col] = df['times'].map(lambda x: formant1.get_value_at_time(formant_number=idx, time=x))
    for idx, col in enumerate(["uF1", "uF2", "uF3"], 1):
        df[col] = df['times'].map(lambda x: formant2.get_value_at_time(formant_number=idx, time=x))

    df['score'] = mapped_score
    data = pd.concat([data, df])

# 결측값 제거
data = data.dropna(axis=0)
print(data)
#print(data)
# 가장 유사도가 낮은 n개의 행 데이터
poor = data.nsmallest(n=30, columns='score',keep='all')
print(poor)
