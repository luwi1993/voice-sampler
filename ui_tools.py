import sounddevice as sd
import soundfile as sf


def play(path):
    data, fs = sf.read(path)
    sd.play(data, fs)
    status = sd.wait()
    return status

def check_remove():
    _input = input("remove? [y/n]").lower()
    if _input == "y":
        remove = True
    elif _input == "n":
        remove = False
    else:
        print("invalid entry")
        remove = check_remove()
    return remove

def check_successfull(path):
    _input = input("ok? [y/n] p for replay").lower()
    success = True
    if _input == "n":
        success = False
    elif _input == "p":
        play(path)
        success = check_successfull(path)
    elif _input != "y":
        print("invalid entry")
        success = check_successfull(path)
    return success

def check_repeat():
    _input = input("repeat? [y/n]").lower()
    if _input == "y":
        repeat = True
    elif _input == "n":
        repeat = False
    else:
        print("invalid entry")
        repeat = check_repeat()
    return repeat

def check_finished(path):
    play(path)
    success = check_successfull(path)
    finished = True
    repeat = False
    if not success:
        repeat = check_repeat()
        if repeat:
            finished = False
            repeat = True
        else:
            finished = True
    return finished, success, repeat

def show_transcription(transcription, go_signal):
    print("---"*3+"read this"+"---"*3)
    print(transcription)
    print("---"*9)
    go_signal()
