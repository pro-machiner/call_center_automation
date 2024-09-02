from run_whisper import inference
from summerize_llm import generate_response


def pipeline(audio_path):
    transcription = inference(audio_path)
    summary = generate_response(transcription)

    return transcription, summary
