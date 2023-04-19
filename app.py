import azure.cognitiveservices.speech as speechsdk
import openai
from app_copy import *

# Set up OpenAI API credentials
openai.api_type = "azure"
openai.api_base = api_base
openai.api_version = api_version
openai.api_key = api_key

# Set up Azure Speech-to-Text and Text-to-Speech credentials
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_recognition_language="it-IT"
speech_config.speech_synthesis_language = "it-IT"

# Set up the voice configuration
speech_config.speech_synthesis_voice_name = "it-IT-GianniNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Define the speech-to-text function
def speech_to_text(while_loop: bool = False):

    # Set up the audio configuration
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create a speech recognizer and start the recognition
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    if while_loop == True:
        help_message = "Posso esserti utile in qualche altro modo?"
        print(help_message)

    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "Mi spiace, non ho capito."
    elif result.reason == speechsdk.ResultReason.Canceled:
        return "Recognition canceled."

# Define the text-to-speech function
def text_to_speech(text):
    try:
        result = speech_synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            #print("Text-to-speech conversione avvenuta con successo.")
            return True
        else:
            print(f"Errore durante la sintetizzazione dell'audio: {result}")
            return False
    except Exception as ex:
        print(f"Errore durante la sintetizzazione dell'audio: {ex}")
        return False

# Define the Azure OpenAI language generation function
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        engine=engine_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps people find information about Reti S.p.A."},
            {"role": "user", "content": "What are the strengths of Reti S.p.A.?"},
            {"role": "assistant", "content": "Among the main Italian players in IT consulting; Wide range of services and high skills in KET; Campus owned as a strategic asset; Consolidated customer portfolio and long-term partnerships"},
            {"role": "user", "content": "can you explain the first point?"},
            {"role": "assistant", "content": "RETI, a Benefit Society and B-Corp, is one of the main Italian players in the IT Consulting sector, specializing in System Integration services, and supports Mid & Large Corporate in digital transformation to compete in increasingly global scenarios. RETI is a Benefit company, certified as a B-Corp, which places social and environmental value at the center of its activities. Always attentive to sustainability, RETI is committed to reducing the environmental impact of its activities, promoting social inclusion, and supporting the growth of local communities."},
            {"role": "user", "content": "What does KET means?"},
            {"role": "assistant", "content": "RETI provides IT Solutions, Business Consulting and Managed Service Provider services through the main Key Enabling Technologies (KET): Cyber Security, Big Data & Analytics and AI, IoT, Cloud. Almost 400 highly qualified professionals employed under the National Collective Labour Agreement for Commerce." },
            {"role": "user", "content": "let's talk me about campus"},
            {"role": "assistant", "content": "Constant activity of innovation, training, and technological scouting that is concretized in the \"Campus,\" the internal laboratory of 20,000 square meters divided into 6 centers of competence, a strategic asset that allows the company to be highly competitive, proposing innovative solutions on the IT Consulting market."},
            #{"role": "user", "content": ""},
            #{},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    #print(response)
    return response['choices'][0]['message']['content']

text_to_speech("Buongiorno, come posso esserti utile oggi?")
while_loop = False

# Main program loop
while True:
    # Get input from user using speech-to-text
    user_input = speech_to_text(while_loop)
    print(f"Mi hai detto: {user_input}")
    if "stop" in user_input.lower():
        text_to_speech("ok, buona giornata!")
        break

    text_to_speech("Dammi un momento...")

    # Generate a response using OpenAI
    prompt = f"Q: {user_input}\nA:"
    response = generate_text(prompt)
    #response = user_input
    print(f"AI risponde: {response}")

    # Convert the response to speech using text-to-speech
    text_to_speech(response)

    while_loop = True
