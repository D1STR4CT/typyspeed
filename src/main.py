from pynput.keyboard import Key, Listener
from time import time, sleep
import os 
import linecache


def add_to_log(log): 
    with open("logfile.txt", "a") as f:
        f.write(log)

def on_press(key):
    log = f"{key} {time()} \n"
    add_to_log(log)

def on_release(key):
    if key == Key.esc:
        return False

def count_keys():
    total_presses = 0
    with open("logfile.txt", "r") as f:
        for _ in f.readlines():
            total_presses += 1

    total_presses = total_presses
    # print(total_presses)

    starttime_line = linecache.getline("logfile.txt", 1)
    starttime_list = starttime_line.split()
    # print(starttime_list)
    starttime = starttime_list[1]

    endtime_line = linecache.getline("logfile.txt", total_presses)
    endtime_list = endtime_line.split()
    # print(endtime_list)
    endtime = endtime_list[1]

    total_time = float(endtime) - float(starttime)

    cps = total_presses/total_time
    cpm = cps*60

    print(f"{total_presses} keys in {total_time}. CPM: {cpm}")

    os.remove("logfile.txt")

# with Listener(
#     on_press = on_press,
#     on_release = on_release
# ) as listener:
#     listener.join()

listener = Listener(on_press=on_press, on_release=on_release)



listener.start()

sleep(30)

listener.stop()

count_keys()
