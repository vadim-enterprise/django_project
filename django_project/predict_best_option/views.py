# chatbot_app/views.py

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import speech_recognition as sr
from openai import OpenAI

def index(request):
    return render(request, 'predict_best_option/index.html')

def process_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        fs = FileSystemStorage()
        filename = fs.save(audio_file.name, audio_file)
        file_url = fs.url(filename)
        file_path = fs.path(filename)

        # Transcribe the audio file
        transcribed_text = transcribe_audio(file_path)

        api_key = 

        client = OpenAI(api_key=api_key)

        def ask_chatgpt(prompt):

            response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_tokens=1000
                )
            
            print(response)
            print(response.choices[0])
            print(response.choices[0].message.content)
            return response.choices[0].message.content

        # def ask_chatgpt(prompt):
        #     response = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo",
        #         messages=[{"role": "system", "content": prompt}]
        #     )
        #     return response.choices[0].message['content']

        # Generate the summary
        summary_prompt = f"Summarize the following text: {transcribed_text}"
        summary_output = ask_chatgpt(summary_prompt)

        # Generate insights
        insights_prompt = f"Provide key insights from the following text: {transcribed_text}"
        insights_output = ask_chatgpt(insights_prompt)

        # Generate next steps or recommendations
        recommendations_prompt = f"Based on this transcription, provide recommendations for the company" #: {company_description}
        recommendations_output = ask_chatgpt(recommendations_prompt)

        # Step 3: Render the results in the template
        return render(request, 'predict_best_option/index.html', {
            'transcribed_text': transcribed_text,
            'summary_output': summary_output,
            'insights_output': insights_output,
            'recommendations_output': recommendations_output,
        })

    return render(request, 'predict_best_option/index.html')

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)
    with audio_file as source:
        audio_data = recognizer.record(source)
    try:
        transcribed_text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        transcribed_text = "Could not understand audio."
    except sr.RequestError:
        transcribed_text = "Could not request results from the speech recognition service."
    return transcribed_text

def generate_summary(text):
    # Placeholder for summary logic
    return f"Summary of the text: {text[:100]}..."  # Truncate for example

def generate_insights(text):
    # Placeholder for insights logic
    return f"Insights based on the text: {text[:100]}..."  # Truncate for example

def generate_recommendations(text):
    # Placeholder for recommendations logic
    return f"Recommendations: {text[:100]}..."  # Truncate for example




