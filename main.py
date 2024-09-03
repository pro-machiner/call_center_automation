from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
import whisper
from summerize_llm import generate_response

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

model = whisper.load_model("tiny")
words = open("dictionary.txt").readline().strip()

class TranscriptionRequest(BaseModel):
    transcription: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/start-transcription")
async def start_transcription(file: UploadFile = File(...)):
    if not os.path.exists("temp"):
        os.makedirs("temp")

    temp_file_path = f"temp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = model.transcribe(temp_file_path, initial_prompt=words)
        transcription = result["text"]
    finally:
        os.remove(temp_file_path)

    return {"transcription": transcription}

@app.post("/get-summary")
async def get_summary(request: TranscriptionRequest):
    try:
        print(request.transcription)
        summary = generate_response(request.transcription)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
