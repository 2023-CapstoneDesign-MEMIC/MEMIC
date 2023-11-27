from django.shortcuts import render

import librosa
import librosa.display
from fastdtw import fastdtw
import pandas as pd
import numpy as np
import parselmouth
from sklearn.neighbors import KNeighborsClassifier, KDTree
from sklearn.metrics.pairwise import cosine_similarity

# row 생략 없이 출력
pd.set_option('display.max_rows', None)
# col 생략 없이 출력
pd.set_option('display.max_columns', None)
formantVowelData = pd.read_csv('becker_train_data.csv', sep='\t')

for col in ['f1', 'f2', 'f3']:
    formantVowelData[col].fillna(formantVowelData.groupby('vowel')[col].transform('mean'), inplace=True)

# mfcc기반 유사도 점수 계산 함수
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

    return dtwDist, dtwSeq, combined_similarity_percent, cosine_similarity_percent

def l2m(l):
    return np.array(l).reshape(1, -1)

def formant_vowel(fa):
    formant_tree = KDTree(formantVowelData[['f1', 'f2', 'f3']])
    formant_classifier = KNeighborsClassifier(7)
    formant_classifier.fit(X=formantVowelData[['f1', 'f2', 'f3']], y=formantVowelData['vowel'])

    newdata = l2m([fa[0], fa[1], fa[2]])
    result = formant_classifier.predict(newdata)[0]
    return result

def feedback(sV, uV):
    """
    1. **Vowel Height (높이)**: Ranges from high (고모음) to low (저모음). It indicates how close the tongue is to the roof of the mouth.
       - 0: Low
       - 1: Near-low
       - 2: Lower-mid
       - 3: Mid
       - 4: Upper-mid
       - 5: Near-high
       - 6: High

    2. **Vowel Backness (기울기)**: Ranges from front (전설) to back (후설). It indicates the position of the tongue during the articulation of the vowel.
       - 0: Back
       - 1: Near-back
       - 2: Central
       - 3: Near-front
       - 4: Front

    3. **Lip Rounding (입술 모양)**: Indicates whether the lips are rounded or not.
       - 0: Unrounded
       - 1: Rounded

    - 'a' (Open front unrounded vowel): [0, 4, 0]
    - 'æ' (Near-open front unrounded vowel): [1, 4, 0]
    - 'ɑ' (Open back unrounded vowel): [0, 0, 0]
    - 'ɒ' (Open back rounded vowel): [0, 0, 1]
    - 'e' (Close-mid front unrounded vowel): [4, 4, 0]
    - 'ə' (Mid-central vowel): [3, 2, 0]
    - 'ɛ' (Open-mid front unrounded vowel): [2, 4, 0]
    - 'ɤ' (Close-mid back unrounded vowel): [4, 0, 0]
    - 'i' (Close front unrounded vowel): [6, 4, 0]
    - 'ɪ' (Near-close near-front unrounded vowel): [5, 3, 0]
    - 'ɨ' (Close central unrounded vowel): [6, 2, 0]
    - 'o' (Close-mid back rounded vowel): [4, 0, 1]
    - 'ø' (Close-mid front rounded vowel): [4, 4, 1]
    - 'œ' (Open-mid front rounded vowel): [2, 4, 1]
    - 'ɔ' (Open-mid back rounded vowel): [2, 0, 1]
    - 'ɵ' (Close-mid central rounded vowel): [4, 2, 1]
    - 'u' (Close back rounded vowel): [6, 0, 1]
    - 'ɯ' (Close back unrounded vowel): [6, 0, 0]
    - 'ʊ' (Near-close near-back rounded vowel): [5, 1, 1]
    - 'ʌ' (Open-mid back unrounded vowel): [2, 0, 0]
    - 'y' (Close front rounded vowel): [6, 4, 1]
    - 'ʏ' (Near-close near-front rounded vowel): [5, 3, 1]

    s - u를 계산해서
    일치하면 생략
    +면 혀를 위로, -면 혀를 아래로
    +면 혀를 앞으로, -면 혀를 뒤로
    +면 입술을 오므리고, -면 입술을 펴고
    """

    # vowel 종류 22가지
    classed = ['a', 'æ', 'ɑ', 'ɒ', 'e', 'ə', 'ɛ', 'ɤ', 'i', 'ɪ', 'ɨ',
               'o', 'ø', 'œ', 'ɔ', 'ɵ', 'u', 'ɯ', 'ʊ', 'ʌ', 'y', 'ʏ']
    # 높이 : 0 - 저모음, 1 - 근저모음, 2 - 중저모음, 3 - 중모음, 4 - 중고모음, 5 - 근고모음, 6 - 고모음
    # 기울기 : 0 - 후설, 1 - 근후설, 2 - 중설, 3 - 근전설, 4 - 전설
    # 입술 모양 : 0 - 평순, 1 - 원순

    # 혀와 입술 모양 enum 배열으로 매핑
    # tongue_height, tongue_slope, lip_shape
    # tongue_height[uv[mapped_vowels]] << 피드백 구문 호출
    mapped_vowels = {
        'a': [0, 4, 0], 'æ': [1, 4, 0], 'ɑ': [0, 0, 0], 'ɒ': [0, 0, 1],
        'e': [4, 4, 0], 'ə': [3, 2, 0], 'ɛ': [2, 4, 0], 'ɤ': [4, 0, 0],
        'i': [6, 4, 0], 'ɪ': [5, 3, 0], 'ɨ': [6, 2, 0], 'o': [4, 0, 1],
        'ø': [4, 4, 1], 'œ': [2, 4, 1], 'ɔ': [2, 0, 1], 'ɵ': [4, 2, 1],
        'u': [6, 0, 1], 'ɯ': [6, 0, 0], 'ʊ': [5, 1, 1], 'ʌ': [2, 0, 0],
        'y': [6, 4, 1], 'ʏ': [5, 3, 1]
    }

    # [0]: ~으로 분류되며, [1]: ~ 위치하고
    tongue_height = {
        0: ['저모음', '혀의 높이를 매우 낮게'],
        1: ['근저모음', '혀의 높이를 낮게'],
        2: ['중저모음', '혀의 높이를 약간 낮게'],
        3: ['중모음', '혀의 높이를 가운데'],
        4: ['중고모음', '혀의 높이를 약간 높게'],
        5: ['근고모음', '혀의 높이를 높게'],
        6: ['고모음', '혀의 높이를 매우 높게']
    }

    tongue_slope = {
        0: ['후설모음', '혀끝의 위치를 매우 뒤 쪽(성대에 가깝게)에'],
        1: ['근후설모음', '혀끝의 위치를 뒤 쪽(성대에 가깝게)에'],
        2: ['중설모음', '혀끝의 위치를 가운데'],
        3: ['근전설모음', '혀끝의 위치를 앞 쪽(입술에 가깝게)에'],
        4: ['전설모음', '혀끝의 위치를 매우 앞 쪽(입술에 가깝게)에']
    }

    lip_shape = {
        0: ['평순모음', '입술을 오므리지 않고 평평한 모양으로'],
        1: ['원순모음', '입술을 동그랗게 오므리고']
    }

    movement = ""
    if mapped_vowels[sV][0] - mapped_vowels[uV][0] > 0: # 따라하려는 게 혀가 더 높다!
        movement += "혀의 높이를 더 높게 올리고, "
    elif mapped_vowels[sV][0] - mapped_vowels[uV][0] < 0:
        movement += "혀의 높이를 더 낮게 내리고, "
    else:
        movement += "혀의 높이는 그대로 하고, "

    if mapped_vowels[sV][1] - mapped_vowels[uV][1] > 0: # 따라하려는 게 혀가 더 앞쪽!
        movement += "혀끝의 위치를 더 앞 쪽으로 옮기고, "
    elif mapped_vowels[sV][1] - mapped_vowels[uV][1] < 0:
        movement += "혀끝의 위치를 더 뒤 쪽으로 옮기고, "
    else:
        movement+= "혀끝의 위치는 그대로 하고, "

    if mapped_vowels[sV][2] - mapped_vowels[uV][2] > 0:  # 따라하려는 게 원순 나는 평순
        movement+= "입술을 오므려서 발음하세요."
    elif mapped_vowels[sV][2] - mapped_vowels[uV][2] < 0:
        movement+= "입술을 오므리지 않고 발음하세요."
    else:
        movement+= "입술의 모양은 그대로 하고 발음하세요."

    sentence1 = ""
    sentence1 += "따라하려는 음성은 " + sV + " 발음에 가깝고, "
    sentence1 += "사용자님의 음성은 " + uV + " 발음에 가까워요.\n"

    # 높이 / 기울기 / 입술 모양
    sentence2 = ""

    sentence2 += ("따라하려는 음성의 " + sV + "는 "
                  + tongue_height[mapped_vowels[sV][0]][0] + "으로 분류되며, ")
    sentence2 += tongue_height[mapped_vowels[sV][0]][1] + " 위치해야 하고, "
    sentence2 += tongue_slope[mapped_vowels[sV][1]][0] + "으로 분류되며, "
    sentence2 += tongue_slope[mapped_vowels[sV][1]][1] + " 위치해야 합니다.\n"

    sentence2 += ("사용자님의 음성인 " + uV + "는 "
                  + tongue_height[mapped_vowels[uV][0]][0] + "으로 분류되며, ")
    sentence2 += tongue_height[mapped_vowels[uV][0]][1] + " 위치한 상태고, "
    sentence2 += tongue_slope[mapped_vowels[uV][1]][0] + "으로 분류되며, "
    sentence2 += tongue_slope[mapped_vowels[uV][1]][1] + " 위치한 상태입니다.\n"

    sentence2 += "더 높은 점수를 얻으려면... "
    sentence2 += movement

    return sentence1, sentence2

# 메인 함수
def FormantAnalys(request):
    #if request.method == 'POST':

    audio_file1 = 'sourceVocal.wav'
    audio_file2 = 'userVocal.wav'
    y1, sr1 = librosa.load(audio_file1)
    y2, sr2 = librosa.load(audio_file2)

    sound1 = parselmouth.Sound("sourceVocal.wav")
    sound2 = parselmouth.Sound("userVocal.wav")

    # dtw 거리, dtw 배열, 전체 구간 유사도
    distance, path, similarity_ALL, _ = compute_similarity(y1, sr1, y2, sr2)

    # 'sourceVocal.wav'의 parselmouth.Sound 객체 생성 코드
    # 여기서 sound 초기화할 때 DTW로 매핑된 시작지점 - 끝지점으로 잘라서 초기화. << 아이디어 보류

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
    #print(similarity_ALL)

    for mapped in path:
        # DTW 결과에서 가져온 idx1 : sourceVocal.wav의 인덱스, idx2 : userVocal.wav의 인덱스
        idx1, idx2 = mapped

        # 해당 인덱스에 대한 실제 시간.
        time_audio1 = librosa.frames_to_time(idx1, sr=sr1)
        time_audio2 = librosa.frames_to_time(idx2, sr=sr2)

        # 그 시간에서 0.1초만큼 컷팅
        mapped_sound1 = sound1.extract_part(from_time=time_audio1, to_time=time_audio1 + 0.1)
        mapped_sound2 = sound2.extract_part(from_time=time_audio2, to_time=time_audio2 + 0.1)

        # 0.1초만큼 컷팅한 부분 Formant 추출 -> 0.1초 한 구간의 평균값만 나옴.
        formant1 = mapped_sound1.to_formant_burg(time_step=0.1)
        formant2 = mapped_sound2.to_formant_burg(time_step=0.1)

        mapped_y1, mapped_sr1 = librosa.load(audio_file1, offset=time_audio1, duration=0.1)
        mapped_y2, mapped_sr2 = librosa.load(audio_file2, offset=time_audio2, duration=0.1)

        _d1, _d2, _Nonuse, mapped_score = compute_similarity(mapped_y1, mapped_sr1, mapped_y2, mapped_sr2)

        # pitch 추출
        pitch1 = mapped_sound1.to_pitch()
        pitch2 = mapped_sound2.to_pitch()

        df = pd.DataFrame({"times": formant1.ts()}, index=[idxnum])
        idxnum += 1
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
        #print(mapped_score)

    # 결측값 제거
    data = data.dropna(axis=0)
    # print(data)
    # 가장 유사도가 낮은 n개의 행 데이터
    poor = data.nsmallest(n=3, columns='score', keep='all')
    #print(poor)

    sourceVowel = []
    userVowel = []
    for i in range(3):
        sourceFA =[]
        userFA = []
        for j in (["sF1", "sF2", "sF3"]):
            formant_temp = poor.iloc[i][j]
            sourceFA.append(formant_temp)
        for j in (["uF1", "uF2", "uF3"]):
            formant_temp = poor.iloc[i][j]
            userFA.append(formant_temp)

        sourceVowel.append(formant_vowel(sourceFA))
        userVowel.append(formant_vowel(userFA))

    feedback_time = []
    feedback_score = []
    feedback_sentence_ALL = []
    for i in range(3):
        feedback_time.append(poor.iloc[i]["sTimes"])
        feedback_score.append(poor.iloc[i]["score"])
        # 보고서 최초 기본 안내
        # "좋은 성대모사는 모음 포먼트 값이 비슷합니다."
        # "저희는 모음 포먼트 값을 기준으로 보고서를 제공합니다."
        # "점수를 높게 받았지만 만족스럽지 않다면, 목소리의 굵기나 목소리 크기 차이가 있기 때문입니다."
        # "모든 부분에서 점수가 높지 않더라도 훌륭한 성대모사가 될 수 있습니다. 따라하려는 목소리의 특징적인 부분만 높은 점수를 받아도 충분합니다."
        feedback_sentence, detail_sentence = feedback(sourceVowel[i], userVowel[i])
        feedback_sentence_ALL.append(feedback_sentence+detail_sentence)

    print("전체 유사도 : ", similarity_ALL, "%")
    print("----------피드백 보고서-----------")
    for i in range(3):
        print(i+1, "순위 Feedback")
        print("시간 : ", feedback_time[i], "초에서")
        print("점수 : ", feedback_score[i], "%")
        print(feedback_sentence_ALL[i])
        print("\n")

    # STT > 오류 발생 잦음... 특히 성대모사의 경우 발음이 뭉개지는 등의 경우가 많아
    # r = sr.Recognizer()
    # stt = sr.AudioFile(audio_file2)
    # with stt as source:
    #     sttAudio = r.record(source)
    # r.recognize_google(audio_data=sttAudio, language='ko-KR')

    # 아래의 변수들 "JSON" 형태로 return
    # similarity_ALL, feedback_time[], feedback_score[], feedback_sentence_ALL[]
    return render(request, 'formant_analyse.html')
