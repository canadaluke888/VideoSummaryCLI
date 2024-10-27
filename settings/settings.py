import json
import os


class Settings:
    def __init__(self):

        self.settings_file_path = os.path.join(os.path.dirname(__file__), "settings.json")
        self.current_settings = self.load_settings()

    def handle_settings(self):

        print(f"\nCurrent Settings: \n{self.current_settings}")

        while True:

            setting = input("\nEnter a setting: ")

            if setting == 'openai_api_key':
                api_key = input("\nEnter OpenAI API Key: ")

                if api_key.lower() is "cancel" or "":
                    print("Cancelling settings change...")
                    continue

                self.set_openai_api_key(api_key)
                print("\nAPI key set.")

            if setting == 'max_frames':

                max_frames = int(input("\nEnter the max number of frames (1-10): "))

                if max_frames > 10 or max_frames < 1:
                    print("Error. Frame value out of range.")
                elif str(max_frames).lower() == "cancel" or "":
                    print("\nCancelling settings change...")
                    continue

                self.set_max_frames(max_frames)
                print("\nMax frames set.")

            if setting.lower() == 'exit':
                print("\nExiting Settings...")
                break

            if setting not in ["openai_api_key", "max_frames", "exit"]:
                print("\nInvalid input.")
                continue

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