from typing import List
from openai import OpenAI
from settings.settings import Settings
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel

class Summarize:

    def __init__(self):

        self.console = Console()

        self.settings = Settings()

        self.client = OpenAI(api_key=self.settings.get_openai_api_key())

    def get_audio_transcript(self, audio_chunks_paths: List[str]) -> str:

        self.console.print(Panel("[bold][red]Getting audio transcripts...[/red][/bold]", title_align='center', title="Information", border_style='white'))

        full_transcription = []

        # Initialize tqdm with the total number of audio chunks
        with tqdm(total=len(audio_chunks_paths), desc="Transcribing audio chunks", unit="Chunks", colour='yellow') as pbar:
            for chunk_path in audio_chunks_paths:
                with open(chunk_path, "rb") as audio_file:
                    # Transcribe the audio chunk
                    response = self.client.audio.transcriptions.create(
                        model='whisper-1',
                        file=audio_file
                    )
                    transcription = response.text
                    full_transcription.append(transcription)

                # Update the progress bar
                pbar.update(1)

                # Combine all chunk transcriptions
                combined_transcription = " ".join(full_transcription)

        return combined_transcription

    def summarize_transcript(self, audio_transcript: str) -> str:

        self.console.print(Panel("[bold][red]Summarizing Transcript...[/red][/bold]", title_align='center', title="Information", border_style='white'))

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the text from the user."
                },
                {
                    "role": "user",
                    "content": audio_transcript
                }
            ]
        )

        audio_transcript_summary = response.choices[0].message.content

        return audio_transcript_summary

    def describe_video_from_frames(self, encoded_frames: List[str], max_frame_messages: int = 11) -> str:

        self.console.print(Panel("[bold][red]Getting video description from frames...[/red][/bold]", title_align='center', title="Information", border_style='white'))

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Based on the frames from the video, describe what was going on in the video."
                    }
                ]
            }
        ]

        for encoded_frame in encoded_frames:
            messages[0]['content'].append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_frame}"}})

        if len(messages[0]['content']) > max_frame_messages:
            raise ValueError("Number of frame inputs too high. Please lower the frame count.")

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        video_description_from_frames = response.choices[0].message.content

        return video_description_from_frames

    def write_overall_summary(self, video_description: str, audio_transcription_summary: str) -> str:

        self.console.print(Panel("[bold][red]Writing final summary...[/red][/bold]", title="Information", title_align='center', border_style='white'))

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Based on the description from the video and the summary from the audio transcript sent by the user, write an overall summary that combines the visual description and the audio description to get the full summarized picture of what is happening in the video. "
                },
                {
                    "role": "user",
                    "content": f"Video Description: \n{video_description}"
                },
                {
                    "role": "user",
                    "content": f"Audio Transcript Summary: \n{audio_transcription_summary}"
                }
            ]
        )

        overall_summary = response.choices[0].message.content

        return overall_summary


