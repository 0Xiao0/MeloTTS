import os
import uvicorn
from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel
from fastapi.responses import FileResponse
from melo.api import TTS
from dotenv import load_dotenv
import tempfile

load_dotenv()
DEFAULT_SPEED = float(os.getenv('DEFAULT_SPEED', '1.0'))  # 默认语速 1.0
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'EN')    # 默认语言 'EN'
DEFAULT_SPEAKER_ID = os.getenv('DEFAULT_SPEAKER_ID', '0') # 默认说话人 ID '0'
device = 'auto' # Will automatically use GPU if available

class TextModel(BaseModel):
    text: str
    speed: float = DEFAULT_SPEED
    language: str = DEFAULT_LANGUAGE
    speaker_id: str = DEFAULT_SPEAKER_ID

app = FastAPI()

def get_tts_model(body: TextModel):
    return TTS(language=body.language, device=device)

@app.post("/convert/tts")
async def create_upload_file(body: TextModel = Body(...), model: TTS = Depends(get_tts_model)):
    speaker_ids = model.hps.data.spk2id

    # Create a temporary file
    output_path = body.language + "_" + body.speaker_id + ".wav"
    model.tts_to_file(body.text, speaker_ids[body.speaker_id], output_path, speed=body.speed)

    # Create a temporary file
    output_path = body.language + "_" + body.speaker_id + ".wav"
    model.tts_to_file(body.text, speaker_ids[body.speaker_id], output_path, speed=body.speed)

    print(os.path.basename(output_path))
    # Return the audio file
    response = FileResponse(output_path, media_type="audio/mpeg", filename=os.path.basename(output_path))

    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
