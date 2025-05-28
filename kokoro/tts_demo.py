import soundfile as sf
from kokoro import KPipeline
from IPython.display import display, Audio
import pygame
import time
import threading

def main():
    pygame.mixer.init()

    while True:
        text = input("Please enter the text you want to synthesize: ")
        while True:
            additional_text = input("Enter additional text or type 'READY' to finish: ")
            if additional_text.strip().upper() == "READY":
                break
            text += " " + additional_text

        pipeline = KPipeline(lang_code='a')
        generator = pipeline(text, voice='af_heart')
        for i, (gs, ps, audio) in enumerate(generator):
            print(i, gs, ps)
            display(Audio(data=audio, rate=24000, autoplay=i == 0))
            sf.write(f'{i}.wav', audio, 24000)

        print("Audio saved to output.wav")

        pygame.mixer.music.load("0.wav")
        time.sleep(1)
        pygame.mixer.music.play()

        # Flags for controlling input and exit
        paused = False
        playback_finished = False

        def listen_for_input():
            nonlocal paused, playback_finished
            while not playback_finished:
                user_input = input("Press 'S' to pause, 'R' to resume: ").strip().upper()
                if user_input == 'S':
                    pygame.mixer.music.pause()
                    paused = True
                    print("Paused.")
                elif user_input == 'R':
                    pygame.mixer.music.unpause()
                    paused = False
                    print("Resumed.")

        input_thread = threading.Thread(target=listen_for_input, daemon=True)
        input_thread.start()

        while pygame.mixer.music.get_busy() or paused:
            time.sleep(0.1)

        playback_finished = True
        print("Playback finished.")

        again = input("Would you like to synthesize another sentence? (Y/N): ").strip().upper()
        if again != 'Y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()