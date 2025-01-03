import whisper
from pydub import AudioSegment
import re

# Define constants
AUDIO_FILE = "audio.wav"
BLACKLIST_FILE = "blackListedWords.txt"

# This removes punctuation from words, strips them and makes them into lowercase
def clean_word(word):
    return re.sub(r'[^\w\s]', '', word).strip().lower()

def get_timestamps_with_whisper(audio_file, blacklist_file):

    # Load the Whisper model
    model = whisper.load_model("base")

    # Load audio and transcribe with timestamps
    result = model.transcribe(audio_file, word_timestamps=True)

    # Debug: Output full transcription
    print(f"Full Transcription: {result['text']}")

    # Load blacklisted keywords into an array
    with open(blacklist_file, "r") as file:
        keywords = [line.lower().strip() for line in file.readlines()]

    # Find timestamps for blacklisted words
    word_timestamps = []
    for segment in result["segments"]:
        for word_info in segment["words"]:
            word = word_info["word"].lower()
            start_time = word_info["start"]
            end_time = word_info["end"]

            word = clean_word(word)

            # Check if word is blacklisted
            if word in keywords:
                word_timestamps.append((word, start_time, end_time))
                print(f"Keyword '{word}' found from {start_time:.2f}s to {end_time:.2f}s")

    return word_timestamps

# Get timestamps for blacklisted words
# word_timestamps = get_timestamps_with_whisper(AUDIO_FILE, BLACKLIST_FILE)

# Output word timestamps
# print(f"word_timestamps is {word_timestamps}")