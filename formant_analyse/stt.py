import speech_recognition as sr

# 음성 파일 경로
audio_file = "drama_test.wav"

# 음성 파일 로드
r = sr.Recognizer()
with sr.AudioFile(audio_file) as source:
    audio = r.record(source)

# Google Web API를 사용하여 음성인식 수행
try:
    recognized = r.recognize_google(audio)
    print("Recognized Speech:", recognized)
    # 각 단어의 타임스탬프 출력
    for idx, result in enumerate(r.recognize_google(audio, show_all=True)['alternative']):
        print(f"Alternative {idx + 1}:")
        for word in result['words']:
            print(f"Word: {word['word']}, Start Time: {word['start_time']}, End Time: {word['end_time']}")
except sr.UnknownValueError:
    print("Google Web Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Web Speech Recognition service; {0}".format(e))