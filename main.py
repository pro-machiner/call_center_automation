from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
import whisper
from summerize_llm import generate_response


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

model = whisper.load_model("small")
complete_transcription = ""
words = open("dictionary.txt").readlines()[0]



@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.post("/start-transcription")
async def start_transcription(file: UploadFile = File(...)):
    global complete_transcription
    complete_transcription = ""  

    if not os.path.exists("temp"):
        os.makedirs("temp")

    temp_file_path = f"temp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = model.transcribe(temp_file_path, initial_prompt=words)
    complete_transcription = result["text"]

    os.remove(temp_file_path)

    return {"transcription": complete_transcription}

@app.get("/get-summary")
async def get_summary():
    try:
        summary = generate_response(complete_transcription)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
