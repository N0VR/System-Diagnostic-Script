import psutil




#Creating Memory Class
class Memory:
    def __init__(self):
        pass

    #Convert Mem to GB
    def update(self):
        mem = psutil.virtual_memory()
        self.used_gb = mem.used / (1024 ** 3)
        self.available_gb = mem.available / (1024 ** 3)