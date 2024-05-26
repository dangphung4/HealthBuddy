import os
from fastapi import FastAPI, File, UploadFile, WebSocket
from google.cloud import speech

# get api keys from environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Speech2t.json"

app = FastAPI()


client = speech.SpeechClient()

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
    return {"Hello": "World"}

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
        sample_rate_hertz=16000,
        language_code="vi-VN"  # For Vietnamese
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
        sample_rate_hertz=16000,
        language_code="vi-VN"  # Set the language to Vietnamese
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

if __name__ == "__main__":
    transcribe_file("path_to_your_audio_file.wav")
