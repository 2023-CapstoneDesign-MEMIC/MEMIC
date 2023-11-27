# MEMIC

Django version >= 3.0

```
pip install pillow django-bootstrap4 pytube librosa soundfile pydub praat-parselmouth spleeter boto3 django-storages
```
API (임시) <p>
로컬 파일 업로드 > /fileupload <p>
유튜브 추출 > /fileupload/youtube <p>
보고서 > /analyse <p>
관리자 > /admin

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

--------

### 나머지 기능 (서버에 포함되지 않음)
문장형 피드백 알고리즘

