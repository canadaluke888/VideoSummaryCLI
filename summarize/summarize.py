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
        self.console.print(Panel("[bold][red]Getting audio transcripts...[/red][/bold]", title="Information", title_align='center', border_style='white'))

        full_transcription = []

        # Initialize tqdm with the total number of audio chunks
        with tqdm(total=len(audio_chunks_paths), desc="Transcribing audio chunks", unit="Chunks", colour='yellow') as pbar:
            for chunk_path in audio_chunks_paths:
                try:
                    with open(chunk_path, "rb") as audio_file:
                        response = self.client.audio.transcriptions.create(
                            model='whisper-1',
                            file=audio_file
                        )
                        transcription = response.text
                        full_transcription.append(transcription)
                except Exception as e:
                    self.console.print(Panel(f"[bold][red]Error processing {chunk_path}: {str(e)}[/red][/bold]", title="Error", border_style='white'))
                    continue  # Skip the problematic file and continue with others

                # Update the progress bar
                pbar.update(1)

        # Combine all chunk transcriptions
        combined_transcription = " ".join(full_transcription)
        return combined_transcription

    def summarize_transcript(self, audio_transcript: str) -> str:
        self.console.print(Panel("[bold][red]Summarizing Transcript...[/red][/bold]", title="Information", title_align='center', border_style='white'))

        if not audio_transcript:
            self.console.print(Panel("[bold][red]Transcript is empty. Exiting summarization...[/red][/bold]", title="Error", border_style='white'))
            return ""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "Summarize the following transcript:"},
                {"role": "user", "content": audio_transcript}
            ]
        )

        audio_transcript_summary = response.choices[0].message.content
        return audio_transcript_summary

    def describe_video_from_frames(self, encoded_frames: List[str], max_frame_messages: int = 10) -> str:
        self.console.print(
            Panel("[bold][red]Getting video description from frames...[/red][/bold]", title="Information",
                  title_align='center', border_style='white'))

        if not encoded_frames:
            self.console.print(
                Panel("[bold][red]No frames available for description. Exiting...[/red][/bold]", title="Error",
                      border_style='white'))
            return ""

        if len(encoded_frames) > max_frame_messages:
            self.console.print(
                Panel("[bold][red]Frame count exceeds the limit. Reduce frame count and try again.[/red][/bold]",
                      title="Error", border_style='white'))
            return ""

        # Structure the messages
        messages = [
            {"role": "user", "content": "Describe the scene based on the following video frames."}
        ]

        for frame in encoded_frames:
            messages.append({
                "role": "user",
                "content": f"![Video Frame](data:image/jpeg;base64,{frame})"
            })

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        video_description_from_frames = response.choices[0].message.content
        return video_description_from_frames

    def write_overall_summary(self, video_description: str, audio_transcription_summary: str) -> str:
        self.console.print(Panel("[bold][red]Writing final summary...[/red][/bold]", title="Information", title_align='center', border_style='white'))

        if not video_description and not audio_transcription_summary:
            self.console.print(Panel("[bold][red]No description or summary to combine. Exiting...[/red][/bold]", title="Error", border_style='white'))
            return ""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Write an overall summary combining the video description and transcript summary."},
                {"role": "user", "content": f"Video Description: \n{video_description}"},
                {"role": "user", "content": f"Audio Transcript Summary: \n{audio_transcription_summary}"}
            ]
        )

        overall_summary = response.choices[0].message.content
        return overall_summary


