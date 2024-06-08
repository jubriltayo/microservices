from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile

def text_to_speech(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        tts = gTTS(text=text, lang='en')
        tts.save('tts_output.mp3') # saved on the server

        # send file to user's browser
        with open('tts_output.mp3', 'rb') as audio_file:
            response = HttpResponse(audio_file.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="tts_output.mp3"' # The HTTP response header 'Content-Disposition' ensures browser handle file as downloadable attachment
            return response
    return render(request, 'index.html')


# Ensure the uploaded_files directory exists
UPLOAD_DIR = 'uploaded_files'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Set ffmpeg path if not in system PATH
AudioSegment.converter = "C:/Program Files/ffmpeg-7.0.1-essentials_build/bin/ffmpeg.exe"

def speech_to_text(request):
    if request.method == 'POST':
        if 'audio_file' in request.FILES:
            audio_file = request.FILES['audio_file']

             # Create a temporary directory for file processing
            with tempfile.TemporaryDirectory() as tempdir:
                audio_path = os.path.join(tempdir, audio_file.name)

                # Save the uploaded file temporarily
                with open(audio_path, 'wb+') as destination:
                    for chunk in audio_file.chunks():
                        destination.write(chunk)

                try:
                    # Convert the audio file to a format recognized by SpeechRecognition (WAV)
                    sound = AudioSegment.from_file(audio_path)
                    wav_path = os.path.join(tempdir, f"{os.path.splitext(audio_file.name)[0]}.wav")
                    sound.export(wav_path, format="wav")

                    recognizer = sr.Recognizer()

                    # Read the converted WAV file
                    with sr.AudioFile(wav_path) as source:
                        audio = recognizer.record(source)
                        text = recognizer.recognize_google(audio)
                        return JsonResponse({'text': text})
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
                finally:
                    # Temporary directory and its contents will be automatically cleaned up
                    pass
    return render(request, 'speech_to_text.html')