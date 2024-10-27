from extract.extract import Extract
from summarize.summarize import Summarize
from settings.settings import Settings
from rich.panel import Panel
from rich.table import Table
from rich.console import Console

console = Console()
extract = Extract()
summarize = Summarize()
settings = Settings()

command_list = ["summarize", "settings", "exit"]


def main():
    console.print("[blue]Welcome to Video Summary CLI![/blue]")

    while True:
        command = console.input("[red]Enter a command:[/red] ").lower()

        if command == 'summarize':
            video_path = console.input("[orange]Enter path to video:[/orange]")

            # Extract and summarize content
            video_frames = extract.extract_highlight_frames(video_path)
            video_audio_path = extract.extract_audio(video_path)
            audio_transcript = summarize.get_audio_transcript(video_audio_path)
            video_description = summarize.describe_video_from_frames(video_frames)
            audio_transcript_summary = summarize.summarize_transcript(audio_transcript)
            overall_summary = summarize.write_overall_summary(video_description, audio_transcript_summary)

            audio_transcript_panel = Panel(
                audio_transcript,
                title="Audio Transcript",
                title_align='center',
                border_style='red'
            )

            console.print(audio_transcript_panel)


            video_description_panel = Panel(
                video_description,
                title="Video Description From Frames",
                title_align='center',
                border_style='purple'
            )

            console.print(video_description_panel)

            summary_panel = Panel(
                overall_summary,
                title="Summary",
                title_align='center',
                border_style="green"
            )

            console.print(summary_panel)

        elif command == 'settings':
            settings.handle_settings()

        elif command == 'exit':
            break

        elif command not in command_list:
            console.print("[red]\nInvalid command![/red]")
            continue

if __name__ == '__main__':
    main()
