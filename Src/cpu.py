import psutil
import time






#Creating CPU Class
class CPU:
    def __init__(self):
        self.usage = 0.0
        psutil.cpu_percent(interval=None)

    def update(self):
        self.usage = psutil.cpu_percent(interval=0)