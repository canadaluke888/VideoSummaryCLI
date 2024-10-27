from extract.extract import Extract
from summarize.summarize import Summarize
from settings.settings import Settings
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from openai import BadRequestError

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

            if not settings.check_for_api_key():
                console.print(Panel("[bold][red]API Key not set.[/red][/bold]", title='Information', title_align='center', border_style='white'))
                continue

            video_path = console.input("[orange]Enter path to video:[/orange]")

            if video_path.lower() == 'cancel' or video_path == " ":
                console.print(Panel("[bold][red]Cancelling Summarization...[/red][/bold]", title="Information", title_align='center', border_style='white'))
                continue


            try:
                # Extract and summarize content
                video_frames = extract.extract_highlight_frames(video_path)
                video_audio_path = extract.extract_audio(video_path)
                audio_transcript = summarize.get_audio_transcript(video_audio_path)
                video_description = summarize.describe_video_from_frames(video_frames)
                audio_transcript_summary = summarize.summarize_transcript(audio_transcript)
                overall_summary = summarize.write_overall_summary(video_description, audio_transcript_summary)

            except BadRequestError as e:
                console.print(Panel(f"[bold][red]Error while generating summary:[/red] [orange]\n\n{e}[/orange][/bold]", title="Error", title_align='center', border_style='white'))
                continue

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
            console.print(Panel("[bold][red]Invalid Command![/red][/bold]", title="Error", title_align='center', border_style='white'))
            continue

if __name__ == '__main__':
    main()
