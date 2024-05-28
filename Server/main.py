import os
import io
import logging

from fastapi import FastAPI, File, UploadFile, WebSocket, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google.cloud import speech, texttospeech
from dotenv import load_dotenv
from uuid import uuid4
from openai import OpenAI
import openai
import soundfile as sf
from base64 import b64encode
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Get API keys from environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Speech2t.json"
openai.api_key = os.getenv("OPENAI_API_KEY")
# OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.DEBUG)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

class TextToSpeechRequest(BaseModel):
    text: str

class SpeechToChatRequest(BaseModel):
    audio: UploadFile = File(...)
    role: str

class OpenAIRequest(BaseModel):
    text: str
    role: str = "user"  

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


# @app.get("/")
# async def read_root():
#     with open("test1.wav", "rb") as file:
#         return await full_conversation(SpeechToChatRequest(audio=UploadFile(file), role="doctor. you are helping an elderly woman with dementia and alzheimers. you must not let her know that she has these conditions. respond in a way that is easy for her to understand, be reassurin>

# @app.get("/")
# def read_root():
#     transcribe_file("vietnamese.wav")

# @app.get("/")
# async def read_root():
#     with open("Badaudiotest.wav", "rb") as file:
#         return await full_conversation(SpeechToChatRequest(audio=UploadFile(file), role="doctor. ou are a compassionate and patient doctor. You are talking to an elderly woman she has dementia and alzhiemers. You must not let her know that she has these conditions. Respond in a way>



#@app.get("/")
#async def read_root():
#    with open("Badaudiotest.wav", "rb") as file:
#        return await session_conversation(SpeechToChatRequest(audio=UploadFile(file), role="doctor. ou are a compassionate and patient doctor. You are talking to an elderly woman she has dementia and alzhiemers. You must not let her know that she has these conditions. Respond in a w>

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

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
        language_code="vi-VN"  # Set the language to Vietnamese
        # language_code="en-US"  # Set the language to English
    )

    response = speech_client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

# if __name__ == "__main__":
#     transcribe_file("vietnamese.wav")


@app.post("/text-to-speech-en/")
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

@app.post("/quick-viet/")
async def full_conversation(request: SpeechToChatRequest):
    # Convert speech to text
    audio_content = await request.audio.read()
    audio_buffer = io.BytesIO(audio_content)
    
    data, sr = sf.read(audio_buffer)
    
    audio_recognition = speech.RecognitionAudio(content=audio_content)
    

    audio_recognition = speech.RecognitionAudio(content=audio_content)
    stt_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sr,  # Use the sample rate retrieved from the audio file
        language_code="vi-VN"  # Set the language to Vietnamese
    )

    speech_response = speech_client.recognize(config=stt_config, audio=audio_recognition)
    
    transcript = " ".join([result.alternatives[0].transcript for result in speech_response.results])
    
    # print("speech_response:", speech_response.results)
    # print("Speech Recognition Response:")
    # print(speech_response)
    # print("Transcript:", transcript)

    # Generate response using OpenAI
    client = OpenAI()
    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": transcript}, {"role": "assistant", "content": f"Act as a {request.role}"}]
    )
    chat_text = chat_response.choices[0].message.content
    
    
    # print("Transcribed Text:")
    # print(transcript)
    
    # Convert response text back to speech
    tts_input = texttospeech.SynthesisInput(text=chat_text)
    tts_voice = texttospeech.VoiceSelectionParams(
        language_code="vi-VN",
        name="vi-VN-Neural2-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    tts_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    tts_response = tts_client.synthesize_speech(
        input=tts_input,
        voice=tts_voice,
        audio_config=tts_config
    )

    # output_file = "output_audio-bad.mp3"
    # output_file = "output_audio.mp3"
    
    # TODO REMOVE THIS BEFORE PROD
    # with open(output_file, "wb") as f:
    #     f.write(tts_response.audio_content)

    audio_base64 = b64encode(tts_response.audio_content).decode("utf-8")

    return JSONResponse(content={"transcript": transcript, "audio": audio_base64})


@app.post("/session-conversation/")
async def session_conversation(
    audio: UploadFile = File(...), 
    role: str = "user", 
    language: str = "en-US", 
    voice_name: str = None, 
    voice_gender: str = "NEUTRAL", 
    session_id: str = None, 
    end_session: bool = False
):
    if session_id is None:
        session_id = create_session_id()  # Create a new session for each conversation
        sessions[session_id] = []  # Initialize session history
        sessions[session_id].append({"role": "system", "content": "You are a compassionate and patient doctor. You are talking to an elderly woman she has dementia and alzhiemers. You must not let her know that she has these conditions. Respond in a way that is easy for her to understand, be reassuring, and provide simple and clear advice. You must urge these ideas in mind, your patient must listen to their family and friends. She needs to exercise, sleep, eat and drink well. She must take her medicine, and listen to her family. Respond in Vietnamese."})

    if session_id not in sessions:
        sessions[session_id] = []
        sessions[session_id].append({"role": "system", "content": "You are a compassionate and patient doctor. You are talking to an elderly woman she has dementia and alzhiemers. You must not let her know that she has these conditions. Respond in a way that is easy for her to understand, be reassuring, and provide simple and clear advice. You must urge these ideas in mind, your patient must listen to their family and friends. She needs to exercise, sleep, eat and drink well. She must take her medicine, and listen to her family. Respond in Vietnamese."})

    try:
        # Read audio file
        audio_content = await audio.read()
        logging.debug(f"Audio content length: {len(audio_content)} bytes")

        audio_buffer = io.BytesIO(audio_content)
        
        # Read audio data and sample rate using soundfile
        data, sr = sf.read(audio_buffer)
        logging.debug(f"Audio sample rate: {sr}")

        # Prepare audio for Google Cloud Speech-to-Text
        audio_recognition = speech.RecognitionAudio(content=audio_content)
        stt_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sr,  # Use the sample rate retrieved from the audio file
            language_code="vi-VN"  # Set the language to Vietnamese
        )
        
        # Perform speech recognition
        speech_response = speech_client.recognize(config=stt_config, audio=audio_recognition)
        transcript = " ".join([result.alternatives[0].transcript for result in speech_response.results])
        logging.debug(f"Transcript: {transcript}")

        # Store transcript in session history
        sessions[session_id].append({"role": "user", "content": transcript})
        # Generate response using OpenAI, incorporating session context
        client = OpenAI()
        chat_response = client.chat.completions.create(
            model="gpt-4o",  # Assuming using GPT-4
            messages=sessions[session_id]
        )
        chat_text = chat_response.choices[0].message.content

        logging.debug(f"Chat text: {chat_text}")

        # Update session history with the assistant's response
        sessions[session_id].append({"role": "assistant", "content": chat_text})

        # Convert response text back to speech
        tts_input = texttospeech.SynthesisInput(text=chat_text)
        tts_voice = texttospeech.VoiceSelectionParams(
            # language_code=language,
            language_code="vi-VN",
            name="vi-VN-Neural2-D",
            # name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
            # ssml_gender=texttospeech.SsmlVoiceGender[voice_gender]
        )
        tts_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        tts_response = tts_client.synthesize_speech(
            input=tts_input,
            voice=tts_voice,
            audio_config=tts_config
        )

        # Encode the audio response as Base64
        audio_base64 = b64encode(tts_response.audio_content).decode("utf-8")
        logging.debug("Audio response encoded to base64")

        # Clear session after conversation ends
        if end_session:
            del sessions[session_id]

        # Return the transcript and audio response as JSON
        return JSONResponse(content={"transcript": chat_text, "audio": audio_base64})

    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/session-conversation/")
# async def session_conversation(request: SpeechToChatRequest, end_session: bool = False, session_id: str = None, language: str = "en-US", voice_name: str = None, voice_gender: str = "NEUTRAL"):
#     if session_id is None:
#         session_id = create_session_id()  # Create a new session for each conversation
#         sessions[session_id] = []  # Initialize session history

#     if session_id not in sessions:
#         sessions[session_id] = []

#     # Convert speech to text
#     audio_content = await request.audio.read()
#     audio_buffer = io.BytesIO(audio_content)
#     data, sr = sf.read(audio_buffer)
#     audio_recognition = speech.RecognitionAudio(content=audio_content)
#     stt_config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=sr,  # Use the sample rate retrieved from the audio file
#         language_code=language
#     )
#     speech_response = speech_client.recognize(config=stt_config, audio=audio_recognition)
#     transcript = " ".join([result.alternatives[0].transcript for result in speech_response.results])

#     # Store transcript in session history
#     sessions[session_id].append({"role": "user", "content": transcript})

#     # Generate response using OpenAI, incorporating session context
#     client = OpenAI()
#     chat_response = client.chat.completions.create(
#         model="gpt-4o",  # Assuming using GPT-4
#         messages=sessions[session_id]
#     )
#     chat_text = chat_response.choices[0].message.content

#     # Update session history with the assistant's response
#     sessions[session_id].append({"role": "assistant", "content": chat_text})

#     # Convert response text back to speech
#     tts_input = texttospeech.SynthesisInput(text=chat_text)
#     tts_voice = texttospeech.VoiceSelectionParams(
#         language_code=language,
#         name=voice_name,
#         ssml_gender=texttospeech.SsmlVoiceGender[voice_gender]
#     )
#     tts_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
#     tts_response = tts_client.synthesize_speech(
#         input=tts_input,
#         voice=tts_voice,
#         audio_config=tts_config
#     )

#     # output_file = "output_audio-session.mp3"
#     # with open(output_file, "wb") as f:
#     #     f.write(tts_response.audio_content)

#     # Encode the audio response as Base64
#     audio_base64 = b64encode(tts_response.audio_content).decode("utf-8")

#     # Clear session after conversation ends
#     if end_session:
#         del sessions[session_id]

#     # Return the transcript and audio response as JSON
#     return JSONResponse(content={"transcript": transcript, "audio": audio_base64})

@app.post("/openai-chat/")
async def openai_chat(request: OpenAIRequest):
    try:
        # Assuming OPENAI_API_KEY is set in your environment variables
        client = OpenAI()

        # Initialize the conversation history if not already present
        if "conversation_history" not in sessions:
            sessions["conversation_history"] = [
                {
                    "role": "system",
                    "content": "You are a compassionate and patient doctor. You are talking to an elderly woman she has dementia and alzhiemers. You must not let her know that she has these conditions. Respond in a way that is easy for her to understand, be reassuring, and provide simple and clear advice. Respond in Vietnamese."
                }
            ]

        # Add the user's input to the conversation history
        sessions["conversation_history"].append({"role": "user", "content": request.text})

        # Call the chat completion API with the conversation history
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=sessions["conversation_history"]
        )

        # Extract the assistant's response from the API response
        assistant_response = response.choices[0].message.content

        # Add the assistant's response to the conversation history
        sessions["conversation_history"].append({"role": "assistant", "content": assistant_response})

        return {"response": assistant_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))