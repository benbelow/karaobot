import time


class Stopwatch:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time_ns()
        return self

    def elapsed(self):
        return round(time.time_ns() - self.start_time, 0) / 1000000

    def print_elapsed(self, log):
        x = 1
        # UNCOMMENT FOR PERF. DEBUGGING
        # print("" + log + ": " + str(self.elapsed()))

    def split(self, log):
        self.print_elapsed(log)
        self.start()
