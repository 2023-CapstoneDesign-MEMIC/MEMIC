# MEMIC

Django version>=3.0\
```
pip install pillow
pip install django-bootstrap4
pip install pytube
pip install librosa
pip install soundfile
pip install pydub
```

로컬 파일 올리기 > http://127.0.0.1:8000/fileupload <p>
유튜브 따오기 > http://127.0.0.1:8000/fileupload/youtube <p>
관리자 > http://127.0.0.1:8000/admin

--------

### 서버에 구현 된 기능

비디오/오디오 파일 업로드\
유튜브 링크 업로드\
비디오 -> 오디오 변환\

--------

### 나머지 기능

녹음 API\
오디오 -> 데이터 변환\
MFCC 평가 알고리즘\
Formant 선별 알고리즘(DTW)\
Formant 기준 평가 알고리즘\
오디오 높낮이 그래프\
오디오 Formant 그래프\
그래프 비교 기능
