from pynput.keyboard import Key, Listener
from time import time, sleep


def on_press(key):
    global log
    log.append(time())
    return log

def on_release(key):
    if key == Key.esc:
        global avg
        print(avg)
        return False

def count_keys(total_log):
    
    total_presses = len(total_log)

    starttime = total_log[1]
    endtime = total_log[-1]
    
    global log 
    log = []

    total_time = float(endtime) - float(starttime)

    cps = total_presses/total_time
    cpm = cps*60

    print(f"{total_presses} keys in {int(round(total_time, 0))}. CPM: {int(round(cpm, 0))}")
    global avg
    avg_new = cpm 
    avg_old = avg

    if avg == 0:
        avg = cpm 
        return avg 
    else:
        avg = (avg_new+avg_old)/2
        print(f"average is: {int(round(avg, 0))}")
        return avg


log = []
global avg
avg = 0.0

# with Listener(
#     on_press = on_press,
#     on_release = on_release
# ) as listener:
#     listener.join()

listener = Listener(on_press=on_press, on_release=on_release)

listener.start() 

while True:
    loglen = len(log)
    if loglen > 5:
        current_time = time()
        last_log_time = log[-1]
        if current_time - last_log_time > 2.0:
            count_keys(log)
            log = []

