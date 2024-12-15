import os
import tempfile

import azure.cognitiveservices.speech as speechsdk
from tqdm import tqdm


def generate_sounds(entries):
    # It is necessary to inject spaces inbetween each pinyin representation of a character. Otherwise, it will mess up
    # It seems like there is also 'pronunciation' input option, where you can enter pinyin. Here not using it

    # Initialize variables
    errors = []
    characters_used = 0
    pinyins = sorted(list({entry.pinyin.lower() for entry in entries}))

    # Azure Speech Configuration
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = "northeurope"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"

    # Configure audio output format
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio48Khz96KBitRateMonoMp3)

    # Directory to save audio files
    output_directory = "data/pronunciation"
    os.makedirs(output_directory, exist_ok=True)

    # Generate audio for each pinyin
    for pinyin in tqdm(pinyins):
        file_path = os.path.join(output_directory, f"{pinyin}.mp3")

        # Check character limit
        if characters_used >= 2000000:
            tqdm.write(f"Character limit exceeded: {characters_used}")
            break

        # Skip if the file already exists
        if os.path.exists(file_path):
            continue

        # Use a temporary file for synthesis
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file_path = temp_file.name

        try:
            # Configure temporary audio output
            audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_file_path)
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

            # Generate speech synthesis
            speech_synthesis_result = speech_synthesizer.speak_text_async(pinyin).get()

            if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                characters_used += len(pinyin)

                # Move the temporary file to the final destination
                os.rename(temp_file_path, file_path)
            else:
                # Handle synthesis errors
                cancellation_details = speech_synthesis_result.cancellation_details.error_details
                print(cancellation_details)
                errors.append(pinyin)
                os.remove(temp_file_path)  # Clean up temporary file
        except Exception as e:
            print(e)
            errors.append(pinyin)

    # Print summary
    print(f"\nTotal characters used: {characters_used}")
    print(f"Error generating {len(errors)} words:")
    print(errors)

    return
