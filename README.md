# Video Summary CLI

This is a simple CLI application that uses the Vision, Whisper, and Chat models from OpenAI to transcribe the audio, describe what is happening visually in the video and provide a summary of all the events considering the context from the audio transcript and the visual description.

## Prerequisites
- **Install ffmpeg:** `sudo apt update sudo apt install ffmpeg -y`
- **Install Dependencies:** `pip install -r requirements.txt`

## Usage
- **Setting OpenAI API Key:** Type the `settings` command to enter the settings. Type the `openai_api_key` parameter and enter your API key. You may need to restart the application for settings to fully apply.
- **Changing the Amount of Highlight Frames:** Enter the `settings` command to enter the settings. Enter the `max_frames` parameter. Enter the max number of highlight frames that you would like to have extracted. 
- **Summarizing a Video:** Type the `summarize` command, provide a path to the video you would like summarized.
- **Exit:** Enter the `exit` command.