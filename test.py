import warnings
from glob import glob
from tqdm import tqdm
from run_whisper import inference

warnings.filterwarnings("ignore")

files = glob('/Users/mits-mac-001/Downloads/call_center_audios/*.mp3')

output_file_path = 'inference_results.txt'

with open(output_file_path, 'w') as output_file:
    for audio in tqdm(files):
        result = inference(audio)
        output_file.write(f"{audio}: {result}\n")
        print(result, audio)
