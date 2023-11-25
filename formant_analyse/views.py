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

# mfcc기반 유사도 점수 계산 함수
def compute_similarity(y1, sr1, y2, sr2):
    mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1)
    mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2)

    mfcc1 = mfcc1.T
    mfcc2 = mfcc2.T

    # y1, y2(time sequence)에 대한 enumrated index의 mfcc값 DTW, 즉 dtwSeq는 (y1, y2)로 이루어진 배열
    dtwDist, dtwSeq = fastdtw(mfcc1, mfcc2)
    # 코사인 유사도 계산
    cosine_sim = cosine_similarity(mfcc1, mfcc2)

    # 유클리드 거리 계산
    euclidean_dist = np.linalg.norm(mfcc1 - mfcc2)

    # DTW 거리를 비교 데이터 길이에 따라 정규화하여 백분율로 표시
    max_length = max(len(mfcc1), len(mfcc2))
    normalized_dtw_distance = (1 - dtwDist / max_length) * 100

    # 코사인 유사도를 백분율로 표시
    cosine_similarity_percent = np.mean(cosine_sim) * 100

    # 유클리드 거리를 최대 길이에 대한 비율로 정규화하여 백분율로 표시
    max_euclidean_dist = max_length * max_length
    normalized_euclidean_distance = (1 - euclidean_dist / max_euclidean_dist) * 100

    # 유클리드 거리와 코사인 유사도를 가중 평균하여 종합적인 유사성을 백분율로 표시
    alpha = 0.5  # 가중치 (0에서 1 사이의 값)
    combined_similarity_percent = (alpha * normalized_euclidean_distance + (1 - alpha) * cosine_similarity_percent)

    # 결과 출력
    print("Normalized DTW Distance (in %):", normalized_dtw_distance)
    print("Cosine Similarity (in %):", cosine_similarity_percent)
    print("Normalized Euclidean Distance (in %):", normalized_euclidean_distance)
    print("Combined Similarity (in %):", combined_similarity_percent)

    return dtwSeq, dtwDist, combined_similarity_percent

# 두 개의 Sound에서 포먼트 추출 함수
def compute_formantburg(sound1, sound2):
    data1 = pd.DataFrame({
        "times": [],
        "F0(pitch)": [],
        "F1": [],
        "F2": [],
        'F3': [],
        "filename": []
    })

    data2 = pd.DataFrame({
        "times": [],
        "F0(pitch)": [],
        "F1": [],
        "F2": [],
        'F3': [],
        "filename": []
    })

    # 'sourceVocal.wav'의 formant 출력 코드
    formant1 = sound1.to_formant_burg(time_step=0.1)

    # 'userVocal.wav'의 formant 출력 코드
    formant2 = sound2.to_formant_burg(time_step=0.1)

    # Pitch
    pitch1 = sound1.to_pitch()
    pitch2 = sound2.to_pitch()
    df1 = pd.DataFrame({"times": formant1.ts()})
    df2 = pd.DataFrame({"times": formant2.ts()})

    # F1~F3까지 계산
    for idx, col in enumerate(["F1", "F2", "F3"], 1):
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

    return data1, data2

def feedback():
    return 0

# 메인 함수
def FormantAnalys(request):
    audio_file1 = 'sourceVocal.wav'
    audio_file2 = 'userVocal.wav'
    y1, sr1 = librosa.load(audio_file1)
    y2, sr2 = librosa.load(audio_file2)

    # dtw 거리, dtw 배열, 전체 구간 유사도
    distance, path, similarity_ALL = compute_similarity(y1, sr1, y2, sr2)

    # 'sourceVocal.wav'의 parselmouth.Sound 객체 생성 코드
    # 여기서 sound 초기화할 때 DTW로 매핑된 시작지점 - 끝지점으로 잘라서 초기화. << 아이디어 보류

    sound1 = parselmouth.Sound("sourceVocal.wav")
    sound2 = parselmouth.Sound("userVocal.wav")

    # 각 F1~F3 포먼트
    f1, f2 = compute_formantburg(sound1, sound2)

    # TODO : DTW로 맵핑하고, 그 시계열 데이터에 매칭되는 MFCC 유사도 계산한 배열
    # path == dtw 배열(mfcc index) : [(0, 0), (1, 1), ... , (4, 7)]
    # y값 활용할 것!

    formant_array1 = []
    formant_array2 = []
    for mapped in path:
        idx1, idx2 = mapped

        mapped_audio1 = y1[idx1]
        mapped_audio2 = y2[idx2]

        mapped_sound1 = parselmouth.Sound(mapped_audio1)
        mapped_sound2 = parselmouth.Sound(mapped_audio2)

        formant1 = mapped_sound1.to_formant_burg(time_step=0.1)
        formant2 = mapped_sound2.to_formant_burg(time_step=0.1)

        formant_array1.append(formant1)
        formant_array2.append(formant2)


    # TODO : 큰 차이가 난다고 판단하는 기준과 구간 별 피드백 문장 구현 (case)
    # TODO : STT => 발음 case 작성

    # 아래의 변수들 "JSON" 형태로 return
    # combined_similarity_percent_ALL, combined_similarity_percent_P1
    # combined_similarity_percent_P2, combined_similarity_percent_P3
    # feedback_sentence_P1, feedback_sentence_P2, feedback_sentence_P3
    # formant_graph_P1, formant_graph_P2, formant_graph_P3
    return render(request, 'formant_analyse.html')
