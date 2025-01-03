import pydub
import parseAudio

# audio = audio[:start_time * 1000] + AudioSegment.silent(duration=(end_time - start_time) * 1000) + audio[end_time * 1000:]

AUDIO_FILE = "audio.wav"
BLACKLIST_FILE = "blackListedWords.txt"
CENSOR_FILE = "censor_noise.wav"

def generate_censored_audio(audio_file, black_list_file, beep_file):

    word_time_stamps = parseAudio.get_timestamps_with_whisper(audio_file, black_list_file)

    if len(word_time_stamps) == 0:
        print("Your original audio has no black listed words!")
        return

    audio = pydub.AudioSegment.from_file(audio_file)
    beep = pydub.AudioSegment.from_file(beep_file)

    # Process each timestamp and censor the corresponding audio segments
    # Since audio is re-assigned each time, we keep the previous censors too
    for word, start_time, end_time in word_time_stamps:

        duration = (end_time - start_time) * 1000

        beep_segment = beep[:duration]

        audio = (
            audio[:start_time * 1000]
            + beep_segment[:duration]
            + audio[end_time * 1000:]
        )

    # Export the final censored audio
    audio.export("censored_audio.wav", format="wav")

    print("Censored audio generated successfully!")

generate_censored_audio(AUDIO_FILE, BLACKLIST_FILE, CENSOR_FILE)