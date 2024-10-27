from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from rich.panel import Panel
from tqdm import tqdm
import os
from typing import List
import cv2
import base64
from rich.console import Console
from rich.panel import Panel

class Extract:

    def __init__(self):

        self.console = Console()


    def extract_audio(self, video_path: str, chunk_length_sec: int = 120, output_dir: str = "audio_chunks") -> List[str]:

        self.console.print(Panel("[bold][red]Extracting audio segments...[/red][/bold]", title="Information", title_align="center", border_style='white'))

        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"The video file {video_path} does not exist.")

        # Create output directory for audio chunks if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Extract audio from video
        audio_output_path = os.path.join(output_dir, "full_audio.mp3")
        with VideoFileClip(video_path) as video:
            audio = video.audio
            if audio is None:
                raise ValueError("The video file does not contain any audio.")
            audio.write_audiofile(audio_output_path)

        # Split audio into chunks using pydub
        audio = AudioSegment.from_file(audio_output_path, format="mp3")
        audio_chunks_paths = []

        # Calculate the total number of chunks
        total_chunks = len(audio) // (chunk_length_sec * 1000) + (
            1 if len(audio) % (chunk_length_sec * 1000) != 0 else 0)

        # Initialize tqdm with the calculated total
        with tqdm(total=total_chunks, desc="Processing audio chunks", colour='pink') as pbar:
            for i, start in enumerate(range(0, len(audio), chunk_length_sec * 1000)):
                chunk = audio[start:start + (chunk_length_sec * 1000)]
                chunk_path = os.path.join(output_dir, f"chunk_{i}.mp3")
                chunk.export(chunk_path, format="mp3")
                audio_chunks_paths.append(chunk_path)
                pbar.update(1)  # Update the progress bar by 1 for each chunk created

        return audio_chunks_paths

    def extract_highlight_frames(self, video_path, max_frames=10):

        self.console.print(Panel("[bold][red]Extracting highlight frames...[/red][/bold]", title="Information", title_align='center', border_style='white'))

        # Load the video using OpenCV
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Calculate frame interval based on `max_frames`
        interval = max(1, total_frames // max_frames)

        selected_frames = []

        # Initialize tqdm with the number of frames to extract
        with tqdm(total=max_frames, desc="Extracting frames", unit="Frames", colour='yellow') as pbar:
            for i in range(0, total_frames, interval):
                # Set the video position to the desired frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()

                if not ret:
                    break  # Stop if there was an issue reading the frame

                # Convert the frame to base64
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')

                selected_frames.append(frame_base64)

                # Update the progress bar
                pbar.update(1)

                # Stop once we reach the user-defined max frames
                if len(selected_frames) >= max_frames:
                    break

        cap.release()
        return selected_frames