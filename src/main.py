from pynput.keyboard import Key, Listener
from time import time, sleep


def add_to_log(log): 
    with open("logfile.txt", "a") as f:
        f.write(log)

def on_press(key):
    log = f"{key}, {time()} \n"
    print(log)

def on_release(key):
    if key == Key.esc:
        return False

def count_keys():
    with open("logfile.txt", "r") as f: 
        print(f)

# with Listener(
#     on_press = on_press,
#     on_release = on_release
# ) as listener:
#     Listener.join()

listener = Listener(on_press=on_press, on_release=on_release)



listener.start()
sleep(5)
listener.stop()