import whisper
import time

model = whisper.load_model("large")
dict_keywords = open("dictionary.txt", "r").readlines()[0]
print(dict_keywords)


def inference(audio_path):
    tik = time.time()
    result = model.transcribe(audio_path, initial_prompt=dict_keywords)
    inference_time = time.time() - tik
    print(f"Time taken for whisper inference: {inference_time:.2f} seconds")

    # Print full transcription with timestamps
    print("Transcription with timestamps:")
    for segment in result["segments"]:
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        print(f"[{start_time} --> {end_time}] {segment['text']}")

    # Return full transcription text and segments with timestamps
    # return result["text"], result["segments"]
    return result["text"]


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# Example usage
if __name__ == "__main__":
    audio_path = "/Users/mits-mac-001/Downloads/call_center_audios/7001-0116691300-7001-202407311857-4f6875.mp3"
    full_text, segments = inference(audio_path)
    
    print("\nFull transcription:")
    print(full_text)
