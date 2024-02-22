import speech_recognition as sr
import time
import sys

recogniser = sr.Recognizer()
mic = sr.Microphone()

retry = False
running = 0
loop_count = 0
while True:
    if loop_count > 0:
        cont = 0
        message_change = False
        while cont != '':
            if message_change == True:
                cont = input("\nUnrecognised input. Please retry (press Enter to continue or type 'n' to exit)...")
            else:
                cont = input("\nPress Enter to continue (or type 'n' to exit)...")
            if cont == 'n':
                sys.exit()
            message_change = True

    with mic as source:
        if retry:
            print("\nTry again ('break' words weren't recognised)...", end=" ")
        elif not retry:
            print("\nSpeak now...", end=" ")
        audio = recogniser.listen(source)

    speech = recogniser.recognize_google(audio)
    print("\u2714 Speech recorded\n")

    if 'brake' in speech:
        if 'break' in speech:
            retry = False
            new_speech = speech.replace('brake', 'break')
        else:
            retry = False
            new_speech = speech
    elif 'brake' not in speech and 'break' not in speech:
        retry = True
        continue
    else:
        new_speech = speech

    darts = new_speech.split("break")
    darts = [i.strip(" ") for i in darts]
    score = 0
    for i, value in enumerate(darts):
        if 'triple' in value:
            score += 3 * int(value.split("triple ")[1])
        elif 'double' in value:
            score += 2 * int(value.split("double ")[1])
        elif value.isdigit():
            score += int(value)
        else:
            if value == 'for':
                score += 4
            elif value == 'three':
                score += 3
            print("something went wrong")

    running += score
    loop_count += 1

    print(f"\nDarts thrown: {darts}")
    print(f"Score = {score}")
    print(f"\nRunning total = {running}")


# file = sr.AudioFile('harvard.wav')
# with file as source:
#     audio = recogniser.record(source)

# x = recogniser.recognize_google(audio)
# print(x)