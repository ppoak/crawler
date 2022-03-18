from ffmpy3 import FFmpeg
from utils.beautifulio import console

def download_movie_ffmpeg(source_address, save_path):
    download_ffmpeg = FFmpeg(
        inputs={source_address: None},
        outputs={save_path: '-c copy'}
        )
    console.print(f"Running command: [red]{download_ffmpeg.cmd}")
    download_ffmpeg.run()