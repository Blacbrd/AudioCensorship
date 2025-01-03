import pydub
import parseAudio

# audio = audio[:start_time * 1000] + AudioSegment.silent(duration=(end_time - start_time) * 1000) + audio[end_time * 1000:]

AUDIO_FILE = "audio.wav"
BLACKLIST_FILE = "blackListedWords.txt"

def generate_censored_audio(audioFile, blackListFile):

    word_time_stamps = parseAudio.get_timestamps_with_whisper(audioFile, blackListFile)

    if len(word_time_stamps) == 0:
        print("Your original audio has no black listed words!")
        return

    audio = pydub.AudioSegment.from_file(audioFile)

    # Process each timestamp and censor the corresponding audio segments
    # Since audio is re-assigned each time, 
    for word, start_time, end_time in word_time_stamps:

        audio = (
            audio[:start_time * 1000]
            + pydub.AudioSegment.silent(duration=(end_time - start_time) * 1000)
            + audio[end_time * 1000:]
        )

    # Export the final censored audio
    audio.export("censored_audio.wav", format="wav")

    print("Censored audio generated successfully!")

generate_censored_audio(AUDIO_FILE, BLACKLIST_FILE)