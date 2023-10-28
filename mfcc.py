'''
import librosa
import numpy as np


def extract_mfcc(audio_path, n_mfcc=13):
    y, sr = librosa.load(audio_path)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc


def compute_euclidean_distance(mfcc1, mfcc2):
    distance = np.linalg.norm(mfcc1 - mfcc2)
    return distance


def compute_similarity(audio_path1, audio_path2):
    mfcc1 = extract_mfcc(audio_path1)
    mfcc2 = extract_mfcc(audio_path2)

    distance = compute_euclidean_distance(mfcc1, mfcc2)
    return distance

# 사용 예시
audio_path1 = "/Users/baejunjae/Desktop/MEMIC/뚱이 올리버쌤 성대모사 new.wav"
audio_path2 = "/Users/baejunjae/Desktop/MEMIC/스폰지밥 올리버쌤 성대모사 new.wav"
similarity = compute_similarity(audio_path1, audio_path2)
print(f"Similarity: {similarity}")
'''

'''
import librosa
from fastdtw import fastdtw
import numpy as np

# 두 개의 오디오 파일 경로 설정
audio_file1 = "/Users/baejunjae/Desktop/MEMIC/뚱이 올리버쌤 성대모사 new.wav"
audio_file2 = "/Users/baejunjae/Desktop/MEMIC/스폰지밥 올리버쌤 성대모사 new.wav"

# 오디오 파일을 MFCC로 변환
def compute_mfcc(audio_file):
    y, sr = librosa.load(audio_file)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    return mfcc.T  # 전치하여 각 프레임을 시간 기준으로 사용

# MFCC 특징 벡터를 추출
mfcc1 = compute_mfcc(audio_file1)
mfcc2 = compute_mfcc(audio_file2)

# Dynamic Time Warping 계산
distance, path = fastdtw(mfcc1, mfcc2)

# 결과 출력
print("DTW Distance:", distance)
'''
'''
import numpy as np
import librosa


def extract_mfcc(audio_file, n_mfcc=13):
    # 오디오 파일을 로드하고 MFCC를 추출합니다.
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfccs


def compute_euclidean_distance(mfcc1, mfcc2):
    # 두 MFCC 특징 벡터 사이의 유클리드 거리를 계산합니다.
    diff = mfcc1 - mfcc2
    return np.linalg.norm(diff)


def compute_similarity(audio_file1, audio_file2):
    mfcc1 = extract_mfcc(audio_file1)
    mfcc2 = extract_mfcc(audio_file2)

    # 평균 MFCC를 사용하여 유사도를 계산합니다.
    mean_mfcc1 = np.mean(mfcc1, axis=1)
    mean_mfcc2 = np.mean(mfcc2, axis=1)

    distance = compute_euclidean_distance(mean_mfcc1, mean_mfcc2)
    return distance


# 예제
audio_file1 = "/Users/baejunjae/Desktop/MEMIC/뚱이 올리버쌤 성대모사 new.wav"
audio_file2 = "/Users/baejunjae/Desktop/MEMIC/뚱이 올리버쌤 성대모사 new.wav"#"/Users/baejunjae/Desktop/MEMIC/스폰지밥 올리버쌤 성대모사 new.wav"
similarity = compute_similarity(audio_file1, audio_file2)
print(similarity)
'''
'''
import librosa
from fastdtw import fastdtw
import numpy as np
from scipy.spatial.distance import euclidean
# 두 개의 오디오 파일 경로 설정
audio_file1 = "/Users/baejunjae/Desktop/MEMIC/뚱이 올리버쌤 성대모사 new.wav"
audio_file2 = "/Users/baejunjae/Desktop/MEMIC/스폰지밥 올리버쌤 성대모사 new.wav"

# 오디오 파일을 MFCC로 변환
def compute_mfcc(audio_file):
    y, sr = librosa.load(audio_file)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    return mfcc.T  # 전치하여 각 프레임을 시간 기준으로 사용

# MFCC 특징 벡터를 추출
mfcc1 = compute_mfcc(audio_file1)
mfcc2 = compute_mfcc(audio_file2)

# Dynamic Time Warping 계산
distance, _ = fastdtw(mfcc1, mfcc2)

# 두 오디오 파일의 길이 계산
len_audio1 = len(mfcc1)
len_audio2 = len(mfcc2)

# 최대 가능한 DTW 거리 계산
max_possible_distance = max(len_audio1, len_audio2) * max(np.max(mfcc1), np.max(mfcc2))
min_possible_distance = min(len_audio1, len_audio2) * min(np.max(mfcc1), np.max(mfcc2))
print(distance)
print(max_possible_distance)
print(distance / max_possible_distance)
# DTW 거리를 백분율로 정규화
normalized_distance = (1 - ((distance - min_possible_distance) / (max_possible_distance - min_possible_distance)) * 100)

# 결과 출력
print("Normalized DTW Distance (in %):", normalized_distance)
'''
import librosa
from fastdtw import fastdtw
import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity

# 두 개의 오디오 파일 경로 설정
audio_file1 = "/Users/baejunjae/Desktop/MEMIC/뚱이 올리버쌤 성대모사 new.wav"
audio_file2 = "/Users/baejunjae/Desktop/MEMIC/스폰지밥 올리버쌤 성대모사 new.wav"

# 오디오 파일을 MFCC로 변환
def compute_mfcc(audio_file):
    y, sr = librosa.load(audio_file)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    return mfcc.T  # 전치하여 각 프레임을 시간 기준으로 사용

# MFCC 특징 벡터를 추출
mfcc1 = compute_mfcc(audio_file1)
mfcc2 = compute_mfcc(audio_file2)

# Dynamic Time Warping 계산
distance, _ = fastdtw(mfcc1, mfcc2)

# 코사인 유사도 계산
cosine_sim = cosine_similarity(mfcc1, mfcc2)

# 유클리드 거리 계산
euclidean_dist = np.linalg.norm(mfcc1 - mfcc2)

# DTW 거리를 비교 데이터 길이에 따라 정규화하여 백분율로 표시
max_length = max(len(mfcc1), len(mfcc2))
normalized_dtw_distance = (1 - distance / max_length) * 100

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