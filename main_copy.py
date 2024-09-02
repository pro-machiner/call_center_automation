from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
from pipeline import pipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Ensure the temp directory exists
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # Save the uploaded file to a temporary location
    temp_file_path = f"temp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Use the pipeline function to transcribe the audio
    transcription, summary = pipeline(temp_file_path)

    # Remove the temporary file
    os.remove(temp_file_path)

    return {"filename": file.filename, "transcription": transcription, "summary": summary}
