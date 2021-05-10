from pynput.keyboard import Key, Listener
from time import time, sleep

class data_storage: 
    def __init__(self, log=[], avg=0 , corr_avg=0, avg_accuracy=0, backspaces=0):
        self.log = log
        self.avg = avg 
        self.corr_avg = corr_avg
        self.avg_accuracy = avg_accuracy
        self.backspaces = backspaces

    # define getter methods 
    def get_log(self):
        return self.log
    def get_avg(self):
        return self.avg
    def get_corr_avg(self):
        return self.corr_avg
    def get_avg_accuracy(self):
        return self.avg_accuracy
    def get_backspaces(self):
        return self.backspaces

    # define setter methods
    def reset_log(self):
        self.log = []
    def append_log(self, timestamp):
        self.log.append(timestamp)
    def set_avg(self, average):
        self.avg = average 
    def set_corr_avg(self, corrected_average):
        self.corr_avg = corrected_average
    def set_avg_accuracy(self, accuracy ):
        self.avg_accuracy = accuracy 
    def set_backspaces(self):
        self.backspaces += 1
    def reset_backspaces(self):
        self.backspaces = 0

def on_press(key):
    if key == Key.backspace:
        data.set_backspaces()
        data.append_log(time())
    else: 
        data.append_log(time())

def on_release(key):
    if key == Key.esc:
        print(data.get_avg())
        return False

def count_keys():

    # Define variables used in function calculations 
    total_presses = len(data.get_log()) - data.get_backspaces()

    starttime = data.get_log()[1]
    endtime = data.get_log()[-1]

    total_errors = data.get_backspaces()

    # Calculate total time of typing activity for "burst"
    total_time = float(endtime) - float(starttime)

    # Calculate CPM without error correction
    cps = total_presses/total_time
    cpm = cps*60

    # Calculate CPM with error correction 
    corr_presses = total_presses - total_errors 
    corr_cps = corr_presses/total_time
    corr_cpm = corr_cps*60

    # Calculate accuracy
    typing_accuracy = (corr_presses/total_presses)*100

    """A calculation to view words per minute (WPM) will be added later.
    This relies on the average amount of letters in a word and differs per language."""

    # Print cpm to terminal for testing purposes 
    print(f"CPM is: {round(corr_cpm)}. with an accuracy of: {round(typing_accuracy, 2)}%")
    if typing_accuracy < 100:
        print(f"CPM can be improved to {round(cpm)} if accuracy is 100%")
    else: 
        print("CPM can not be improved anymore by reducing errors!")

    """old piece of code I'm leaving in here for possible future testing"""
    # print(f"{total_presses} keys in {int(round(total_time, 0))}. CPM: {int(round(cpm, 0))}")

    # set new average and get old average
    avg_new = cpm 
    # avg_old = data.get_avg()

    # set new corrected average and get old corrected average 
    corr_avg_new = corr_cpm
    corr_avg_old = data.get_corr_avg() 

    # set new average accuracy and get old average accuracy
    accuracy_new = typing_accuracy
    accuracy_old = data.get_avg_accuracy()

    if data.get_avg() == 0:
        data.set_avg(avg_new)
        data.set_corr_avg(corr_cpm)
        data.set_avg_accuracy(accuracy_new)
    else:
        data.set_avg(avg_new)
        corr_avg = (corr_avg_new+corr_avg_old)/2
        data.set_corr_avg(corr_avg)
        avg_accuracy = (accuracy_new/accuracy_old)/2
        data.set_avg_accuracy(avg_accuracy)
        print(f"average is: {int(round(data.get_avg(), 0))}")
        save_avg(round(data.get_corr_avg()), round(data.get_avg_accuracy(), 2), data.get_avg())


def save_avg(corrected_average, accuracy, average):
    with open("average.txt", "w") as write_avg:
        if accuracy < 100:
            message = f"Average is: {data.get_corr_avg()}CPM\nWith an accuracy of: {data.get_avg_accuracy()}%\nAverage with 100% accuracy: {round(average)}CPM"
            write_avg.write(message)
        else: 
            message = f"Average is: {data.get_avg()}CPM\nWith an accuracy of: {data.get_avg_accuracy()}%"
            write_avg.write(message)

def main(): 
    """ old piece of code I'm leaving in here in case I need it"""
    # with Listener(
    #     on_press = on_press,
    #     on_release = on_release
    # ) as listener:
    #     listener.join()

    listener = Listener(on_press=on_press, on_release=on_release)

    listener.start() 

    while True:
        loglen = len(data.get_log())
        avoid_neg = loglen * 0.5
        if loglen > 5 and data.get_backspaces() < avoid_neg:
            current_time = time()
            last_log_time = data.get_log()[-1]
            if current_time - last_log_time > 1.0:
                count_keys()
                data.reset_log()
                data.reset_backspaces()
        elif loglen > 0 and loglen < 5: 
            current_time = time()
            last_log_time = data.get_log()[-1]
            if current_time - last_log_time > 1.0:
                data.reset_log()
                data.reset_backspaces()
        elif data.get_backspaces() > avoid_neg:
            data.reset_backspaces()
            data.reset_log()


data = data_storage()

if __name__ == "__main__":
    main()