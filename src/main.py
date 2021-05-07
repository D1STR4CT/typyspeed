from pynput.keyboard import Key, Listener
from time import time, sleep

def on_press(key):
    if key == Key.backspace:
        global backspaces 
        backspaces = backspaces + 1 
        return backspaces
    else: 
        global log
        log.append(time())
        return log
    

def on_release(key):
    if key == Key.esc:
        global avg
        print(avg)
        return False

def count_keys(total_log, total_backspaces):
    
    # Define variables used in function calculations 
    total_presses = len(total_log)

    starttime = total_log[1]
    endtime = total_log[-1]

    total_errors = total_backspaces

    # Reset tracking variables for next loop actually not even sure if this is used
    global log 
    log = []
    global backspaces
    backspaces = 0 

    # Calculate total time of typing activity for "burst"
    total_time = float(endtime) - float(starttime)

    # Calculate CPM without error correction
    cps = total_presses/total_time
    cpm = cps*60

    # Calculate CPM with errors correction 
    corr_presses = total_presses - total_errors
    corr_cps = corr_presses/total_time
    corr_cpm = corr_cps*60

    # Calculate accuracy
    typing_accuracy = (corr_presses/total_presses)*100

    """A calculation to view words per minute (WPM) will be added later.
    This relies on the average amount of letters in a word and differs per language."""

    # Print cpm to terminal for testing purposes 
    print(f"CPM is: {corr_cpm}. with an accuracy of: {round(typing_accuracy, 2)}")
    if typing_accuracy < 100:
        print(f"CPM can be improved to {cpm} if accuracy is 100%")
    else: 
        print("CPM can not be improved anymore by reducing errors!")

    """old piece of code I'm leaving in here for possible future testing"""
    # print(f"{total_presses} keys in {int(round(total_time, 0))}. CPM: {int(round(cpm, 0))}")

    global avg
    avg_new = corr_cpm 
    avg_old = avg

    if avg == 0:
        avg = corr_cpm 
        return avg 
    else:
        avg = (avg_new+avg_old)/2
        print(f"average is: {int(round(avg, 0))}")
        save_avg(round(avg), round(typing_accuracy, 2), cpm)
        return avg

def save_avg(average, accuracy, cpm):
    with open("average.txt", "w") as write_avg:
        if cpm < 100:
            message = f"Average is: {average}CPM\nWith an accuracy of: {accuracy}%\nAverage with 100% accuracy: {cpm}CPM"
            write_avg.write(message)
        else: 
            message = f"Average is: {average}CPM\nWith an accuracy of: {accuracy}%"
            write_avg.write(message)

def main(): 
    global log 
    log = []
    global avg
    avg = 0.0
    global backspaces
    backspaces = 0 

    """ old piece of code I'm leaving in here in case I need it"""
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
            if current_time - last_log_time > 1.0:
                count_keys(log, backspaces)
                log = []
                backspaces = 0 
        elif loglen > 0: 
            current_time = time()
            last_log_time = log[-1]
            if current_time - last_log_time > 1.0:
                log = []
                backspaces = 0

if __name__ == "__main__":
    main()