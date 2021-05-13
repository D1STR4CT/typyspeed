from pynput.keyboard import Key, Listener
from time import time

class data_storage: 
    def __init__(self, log=[], avg=[] , corr_avg=0, avg_accuracy=0, backspaces=0, total_avg=0, accuracy=[]):
        self.log = log
        self.avg = avg 
        self.corr_avg = corr_avg
        self.avg_accuracy = avg_accuracy
        self.backspaces = backspaces
        self.total_avg = total_avg
        self.accuracy = accuracy

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
    def get_total_avg(self):
        return self.total_avg
    def get_accuracy(self):
        return self.accuracy 

    # define setter methods
    def reset_log(self):
        self.log = []
    def append_log(self, timestamp):
        self.log.append(timestamp)
    def append_avg(self, average):
        self.avg.append(average)
        if len(self.avg) > 12:
            self.avg = self.avg[-12:] # keep list from gettin too long
        else:
            pass 
    def set_corr_avg(self, corrected_average):
        self.corr_avg = corrected_average
    def set_avg_accuracy(self, accuracy ):
        self.avg_accuracy = accuracy 
    def set_backspaces(self):
        self.backspaces += 1
    def reset_backspaces(self):
        self.backspaces = 0
    def set_total_avg(self, new_total_avg):
        self.total_avg = new_total_avg
    def append_accuracy(self, accuracy):
        self.accuracy.append(accuracy)
        if len(self.accuracy) > 12:
            self.accuracy = self.accuracy[-12:] # keep list from getting too long
        else: 
            pass

def on_press(key):
    if key == Key.esc:
        print(data.get_avg())
        return False

def on_release(key):
    if key == Key.backspace:
        data.set_backspaces()
        data.append_log(time())
    else: 
        data.append_log(time())

def calculate_total_average():
    new_total_avg = 0
    for i in data.get_avg():
        new_total_avg = (new_total_avg + i)
    new_total_avg = new_total_avg/len(data.get_avg())
    data.set_total_avg(new_total_avg)

def calculate_average_accuracy():
    avg_accuracy = 0 
    for i in data.get_accuracy():
        avg_accuracy = (avg_accuracy + i)
    avg_accuracy = avg_accuracy/len(data.get_accuracy())
    data.set_avg_accuracy(avg_accuracy)

def calculate_averages():
    total_presses = (len(data.get_log()) - data.get_backspaces())
    total_errors = data.get_backspaces()
    starttime = data.get_log()[1]
    endtime = data.get_log()[-1]

    total_time = float(endtime) - float(starttime)
    cpm = ((total_presses - total_errors)/total_time)*60
    accuracy = ((total_presses - total_errors)/total_presses)*100

    data.append_avg(cpm)
    data.append_accuracy(accuracy)

    print(f"CPM is: {round(data.get_avg()[-1])}. with an accuracy of: {round(data.get_accuracy()[-1], 2)}%")

def save_averages():
    with open("average.txt", "w") as write_avg:
        if data.get_avg_accuracy() < 100:
            message = f"Average is: {round(data.get_total_avg())}CPM\nWith an accuracy of: {round(data.get_avg_accuracy())}%\n"
            write_avg.write(message)
        else: 
            message = f"Average is: {round(data.get_total_avg())}CPM\nWith an accuracy of: 100%"
            write_avg.write(message)

def main(): 
    listener = Listener(on_press=on_press, on_release=on_release)

    listener.start() 

    while True:
        loglen = len(data.get_log())
        avoid_neg = loglen * 0.5
        if loglen > 5 and data.get_backspaces() < avoid_neg:
            current_time = time()
            last_log_time = data.get_log()[-1]
            if current_time - last_log_time > 1.0:
                calculate_averages()
                calculate_total_average()
                calculate_average_accuracy()
                save_averages()
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