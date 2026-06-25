# My first official Python project! Woohoooooooooo :)
# Finally I was able to implement the audio generation part.
# Which, for a rookie like me, was very difficult.
# Not difficult enough to stop me tho :D
# I will Likely not upload anything in the next few days.
# My next project will be graph related and I am doin research on it as I speak.
# I think I have learned the "basics" and I don't have anything to upload on my "Learning-the-basics-Python" repo
# Of course I will keep uploading there as I learn more and more
# But as for now, I will stick with making that graph project first, then I will see where I go from there.

# It was an absolute journey building this project, and I am very proud of it.
# I tried to pull this project off in C first, yeah, I tried. I ran into malloc and syntaxes I had no business learning.
# I only bothered to learn the basics of C because I wanted to know how C handles memory and how to manipulate it.
# That language can't even take proper inputs without me allocating memory for it. Then I ran into some syntaxes and math and I was like "Not today Satan, I am not gonna learn all this just to make a Morse code translator."
# So here I am, with my work in python. Run it, have fun. 

import math
import struct
import wave

morse_code_dict = {
    # No im not padding my code with spaces, I just want it to look nice and organized. If you don't like it, you can go make your own Morse code translator and stop being a hater >:(
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    " ": "/",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "'": ".----.",
    "!": "-.-.--",
    "/": "-..-.",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    '"': ".-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "@": ".--.-.",
    "$": "...-..-",
}

reverse_morse_code_dict = {v: k for k, v in morse_code_dict.items()}


def generate_morse_audio(morse_code, filename="morse_output.wav"):
    """Synthesizes Morse code into a .wav audio file using standard timing rules."""
    sample_rate = 44100
    frequency = 700

    # I went with 0.06 seconds as the base unit duration
    # You can adjust it if you want
    # I even slowed down the dash duration to make it easy to hear
    # If you still need to make it slower...
    # Maybe it's time to shut your device and start counting your days grandpa :D
    # Matter of fact, why are YOU on GitHub in the first place? Go outside and touch grass, you old fossil :D

    unit_duration = 0.06
    dot_duration = unit_duration
    dash_duration = unit_duration * 5 # Duration was increased from 3x to 5x to make it clearer. For authentic experience, change it to unit_duration * 3. If your ears can keep up that is.
    element_gap = unit_duration  # Gap between dots and dashes within a letter. I wanted to do unit_duration * 2 here. But that seemed unnecessary.
    letter_gap = unit_duration * 3
    word_gap = unit_duration * 7  # Gap between words. I would've made it unit_duration * 5. But * 7 sounded just right

    audio_frames = []

    def add_tone(duration):
        num_samples = int(sample_rate * duration)
        for i in range(num_samples):
            sample = math.sin(2 * math.pi * frequency * i / sample_rate)
            packed_sample = struct.pack("<h", int(sample * 32767))
            audio_frames.append(packed_sample)

    def add_silence(duration):
        num_samples = int(sample_rate * duration)
        for _ in range(num_samples):
            audio_frames.append(struct.pack("<h", 0))

    words = morse_code.strip().split(" / ")
    for w_index, word in enumerate(words):
        letters = word.split()
        for l_index, letter in enumerate(letters):
            for e_index, element in enumerate(letter):
                if element == ".":
                    add_tone(dot_duration)
                elif element == "-":
                    add_tone(dash_duration)

                if e_index < len(letter) - 1:
                    add_silence(element_gap)

            if l_index < len(letters) - 1:
                add_silence(letter_gap)

        if w_index < len(words) - 1:
            add_silence(word_gap)

    # Write data to a standard .wav file. Because I am a nice guy, I will not make you download any external libraries to do this. I will just use the built in wave module and struct module to write the audio data to a .wav file. You can thank me later :D
    # Also .wav is superior to mp3, so you should be grateful that I am giving you a high quality audio file :D
    # Haters will say it's too big. Wanna know what else is big? my love for you, you ungrateful piece of garbage :D
    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"".join(audio_frames))

    print(f"\nAudio successfully saved to: {filename}")

print(
    """
 _       __     __                        
| |     / /__  / /________  ____ ___  ___ 
| | /| / / _ \/ / ___/ __ \/ __ `__ \/ _ \
| |/ |/ /  __/ / /__/ /_/ / / / / / /  __/
|__/|__/\___/_/\___/\____/_/ /_/ /_/\___/                                           
"""
)
print("TO\nMORSE CODE TRANSLATOR\n------------------------------------------\n[1] Translation available for only English\n[2] All invalid characters will be skipped\n")
print("Choose translation type:\n[1] Text to Morse code\n[2] Morse code to Text")
translation_type = input("Write here (1 or 2): ")
while translation_type not in ["1", "2"]:
    print("Invalid input. Please enter '1' or '2'.")
    translation_type = input("Write here (1 or 2): ")

match translation_type:
    case "1":
        print("Selected: Text to Morse code\n\n")
        userInput = input("Write here: ").upper()
        result = ""

        for char in userInput:
            if char not in morse_code_dict:
                print(f'"{char}" was skipped. Invalid/no Morse code available.')
                continue
            result += morse_code_dict[char] + " "

        print(f"\nGenerated Morse Code:\n{result}")

        if result.strip():
            generate_morse_audio(result)

    case "2":
        print('Selected: Morse code to Text\nType "?Help" for instructions\n\n')
        userInput = input("Write here: ").lower()
        result = ""
        while userInput == "?help":
            print(
                "Instructions:\n[1] Separate letters in Morse code with spaces\n[2] Separate words with a slash (/)\n[3] All invalid characters will be skipped\n"
            )
            userInput = input("Write here: ").lower()

        for char in userInput.split():
            if char not in reverse_morse_code_dict:
                print(
                    f'"{char}" was skipped. Invalid/no Text character available.'
                )
                continue
            result += reverse_morse_code_dict[char]
        print(result)
