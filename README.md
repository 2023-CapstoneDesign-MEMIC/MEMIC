# MEMIC

Django version >= 3.0
<br> Python version >=3.8 <= 3.10

```
pip install pillow django-bootstrap4 pytube librosa soundfile pydub praat-parselmouth spleeter boto3 django-storages

pip install django-cors-headers
```

---
### API (임시) 
로컬 파일 업로드 > /fileupload <p>
유튜브 추출 > /fileupload/youtube <p>
보고서 > /analyse <p>
관리자 > /admin

--------
/analyse : formant_analyse/views.py
1. (배경음 분리된) 음성 파일 불러오기
2. 두 음성에 대해 DTW
3. DTW path 배열로 매핑된 구간 별 Formant 게산
4. 구간 별 유사도 점수 평가, 유사도 하위 3개 구간 선택
5. Formant-Vowel 데이터셋을 활용해 K-NN Vowel Classification
6. 선택된 Vowel에 대한 Feedback

> return 전체 유사도, 유사도 하위 3개 구간(구간 유사도, 시간, 피드백 문장)

--------
### 서버에 구현 된 기능

비디오/오디오 파일 업로드\
유튜브 링크 업로드\
비디오 -> 오디오 변환\
오디오 -> 데이터 변환\
녹음 API\
유사도 평가 알고리즘\
DTW 매핑 구간 별 Formant 알고리즘\
Formant-Vowel Classification 알고리즘
문장형 피드백 알고리즘

--------

