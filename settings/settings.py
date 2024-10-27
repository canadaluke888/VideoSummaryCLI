import json
import os
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

class Settings:
    def __init__(self):

        self.console = Console()

        self.settings_file_path = os.path.join(os.path.dirname(__file__), "settings.json")
        self.current_settings = self.load_settings()

    def handle_settings(self):
        current_settings_table = Table(title="Current Settings", show_lines=True, border_style='white')
        current_settings_table.add_column("Setting", style='cyan', no_wrap=True)
        current_settings_table.add_column("Value", style="magenta")

        for setting, value in self.current_settings.items():
            current_settings_table.add_row(str(setting), str(value))

        self.console.print(current_settings_table)

        while True:
            setting = self.console.input("\n[green]Enter a setting:[/green]")

            if setting == 'openai_api_key':
                api_key = self.console.input("\n[green]Enter API Key:[/green]")

                # Check if the user wants to cancel
                if api_key.lower() == "cancel" or api_key == "":
                    self.console.print(
                        Panel("[bold][red]Cancelling Settings Change...[/red][/bold]", title="Information",
                              title_align='center', border_style='white'))
                    continue

                # Otherwise, set the API key
                self.set_openai_api_key(api_key)
                self.console.print(
                    Panel("[bold][green]API Key Set![/green][/bold]", title="Information", title_align='center',
                          border_style='white'))

            elif setting == 'max_frames':
                max_frames = self.console.input("[green]Enter the max number of frames (1-10):[/green]")

                # Check if the user wants to cancel
                if max_frames.lower() == "cancel" or max_frames == "":
                    self.console.print(
                        Panel("[bold][red]Cancelling settings change...[/red][/bold]", title="Information",
                              title_align='center', border_style='white'))
                    continue

                # Validate and set max_frames
                try:
                    max_frames = int(max_frames)
                    if max_frames > 10 or max_frames < 1:
                        self.console.print(
                            Panel("[bold][red]Error. Frame value out of range.[/red][/bold]", title="Error",
                                  title_align='center', border_style='white'))
                        continue
                    self.set_max_frames(max_frames)
                    self.console.print(
                        Panel("[bold][green]Max frames set.[/green][/bold]", title="Information", title_align='center',
                              border_style='white'))
                except ValueError:
                    self.console.print(
                        Panel("[bold][red]Please enter a valid integer or type 'cancel'.[/red][/bold]", title="Error",
                              title_align='center', border_style='white'))
                    continue

            elif setting.lower() == 'exit':
                self.console.print(
                    Panel("[bold][red]Exiting Settings...[/red][/bold]", title="Information", title_align='center',
                          border_style='white'))
                break

            elif setting not in ["openai_api_key", "max_frames", "exit"]:
                self.console.print(Panel("[bold][red]Invalid input.[/red][/bold]", title="Error", title_align='center',
                                         border_style='white'))

    def load_settings(self):
        if os.path.exists(self.settings_file_path):
            with open(self.settings_file_path, 'r') as f:
                return json.load(f)

        else:
            return {"openai_api_key": "", "max_frames": 10}

    def save_settings(self):
        with open(self.settings_file_path, 'w') as f:
            json.dump(self.current_settings, f, indent=4)

    def set_openai_api_key(self, api_key: str):
        self.current_settings['openai_api_key'] = api_key
        self.save_settings()

    def get_openai_api_key(self):
        return self.current_settings.get('openai_api_key', "")

    def set_max_frames(self, max_frames: int = 10):
        self.current_settings['max_frames'] = max_frames
        self.save_settings()

    def get_max_frames(self):
        return self.current_settings.get('max_frames', None)

    def check_for_api_key(self) -> bool:
        if self.current_settings['openai_api_key'] is not None:
            return True