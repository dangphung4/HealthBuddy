import os
from fastapi import FastAPI, File, UploadFile, WebSocket, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google.cloud import speech, texttospeech
from dotenv import load_dotenv
from uuid import uuid4
from openai import OpenAI
import openai

load_dotenv()

# Get API keys from environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Speech2t.json"
openai.api_key = os.getenv("OPENAI_API_KEY")
OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPEN_AI_API_KEY)

app = FastAPI()


speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

class TextToSpeechRequest(BaseModel):
    text: str

class SpeechToChatRequest(BaseModel):
    audio: UploadFile = File(...)
    role: str

class OpenAIRequest(BaseModel):
    text: str
    role: str

sessions = {}

def create_session_id():
    return str(uuid4())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            # process data
            await websocket.send_text("Processed data")
    except Exception as e:
        print('Error:', e)
    finally:
        await websocket.close()
        
        
@app.get("/")
def read_root():
    return full_conversation( SpeechToChatRequest( audio=UploadFile( "Adver.wav" ), role="user" ) )

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/speech-to-text/")
async def convert_speech_to_text(audio: UploadFile = File(...)):
    client = speech.SpeechClient()

    audio_content = await audio.read()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        sample_rate_hertz=48000,
        # language_code="vi-VN"  # For Vietnamese
        language_code="en-US"  # For English
    )

    response = client.recognize(config=config, audio=audio)
    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    return {"transcript": transcript}


def transcribe_file(speech_file):
    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        # language_code="vi-VN"  # Set the language to Vietnamese
        language_code="en-US"  # Set the language to English
    )

    response = speech_client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

if __name__ == "__main__":
    transcribe_file("Adver.wav")


@app.post("/text-to-speech/")
async def convert_text_to_speech(request: TextToSpeechRequest):
    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # Specify the language
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # Set the audio format
    )

    # Perform the text-to-speech request
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Return the audio content in the response
    return Response(content=response.audio_content, media_type="audio/mp3")

@app.post("/full-conversation/")
async def full_conversation(request: SpeechToChatRequest):
    # Convert speech to text
    audio_content = await request.audio.read()
    audio_recognition = speech.RecognitionAudio(content=audio_content)
    stt_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US"
    )
    speech_response = speech_client.recognize(config=stt_config, audio=audio_recognition)
    transcript = " ".join([result.alternatives[0].transcript for result in speech_response.results])

    # Generate response using OpenAI
    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": transcript}, {"role": "assistant", "content": f"Act as a {request.role}"}]
    )
    chat_text = chat_response.choices[0].message['content']

    # Convert response text back to speech
    tts_input = texttospeech.SynthesisInput(text=chat_text)
    tts_voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    tts_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    tts_response = tts_client.synthesize_speech(
        input=tts_input,
        voice=tts_voice,
        audio_config=tts_config
    )

    return Response(content=tts_response.audio_content, media_type="audio/mp3")


@app.post("/doctor-conversation/")
async def doctor_conversation(request: SpeechToChatRequest):
    # Convert speech to text
    audio_content = await request.audio.read()
    audio_recognition = speech.RecognitionAudio(content=audio_content)
    stt_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US"
    )
    speech_response = speech_client.recognize(config=stt_config, audio=audio_recognition)
    transcript = " ".join([result.alternatives[0].transcript for result in speech_response.results])

    # Custom prompts for the doctor role
    if "fall" in transcript.lower() or "hurt" in transcript.lower():
        prompt = "As a doctor, provide advice to someone who has fallen and might be hurt."
    else:
        prompt = f"As a doctor, how would you respond to: '{transcript}'?"

    # Generate response using OpenAI
    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    chat_text = chat_response.choices[0].message['content']

    # Convert response text back to speech
    tts_input = texttospeech.SynthesisInput(text=chat_text)
    tts_voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    tts_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    tts_response = tts_client.synthesize_speech(
        input=tts_input,
        voice=tts_voice,
        audio_config=tts_config
    )

    return Response(content=tts_response.audio_content, media_type="audio/mp3")


@app.post("/session-conversation/")
async def session_conversation(request: SpeechToChatRequest):
    session_id = create_session_id()  # Create a new session for each conversation
    sessions[session_id] = []  # Initialize session history

    # Convert speech to text
    audio_content = await request.audio.read()
    audio_recognition = speech.RecognitionAudio(content=audio_content)
    stt_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US"
    )
    speech_response = speech_client.recognize(config=stt_config, audio=audio_recognition)
    transcript = " ".join([result.alternatives[0].transcript for result in speech_response.results])

    # Store transcript in session history
    sessions[session_id].append({"role": "user", "content": transcript})

    # Generate response using OpenAI, incorporating session context
    chat_response = openai.ChatCompletion.create(
        model="gpt-4o",  # Assuming using GPT-4
        messages=sessions[session_id]
    )
    chat_text = chat_response.choices[0].message['content']
    
    # Update session history with the assistant's response
    sessions[session_id].append({"role": "assistant", "content": chat_text})

    # Convert response text back to speech
    tts_input = texttospeech.SynthesisInput(text=chat_text)
    tts_voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    tts_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    tts_response = tts_client.synthesize_speech(
        input=tts_input,
        voice=tts_voice,
        audio_config=tts_config
    )

    # Clear session after conversation ends
    del sessions[session_id]

    return Response(content=tts_response.audio_content, media_type="audio/mp3")

@app.post("/openai-chat/")
async def openai_chat(request: OpenAIRequest):
    try:
        # Assuming OPENAI_API_KEY is set in your environment variables
        client = OpenAI()


        # The correct method to call the chat completion API in openai>=1.0.0
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
        )
        
        return {"response": response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))