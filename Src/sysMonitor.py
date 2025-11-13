from Src.cpu import CPU
from Src.memory import Memory
from Src.drive import Drive
import time
import os
import threading




#Creating SystemMonitor Class / Main
class SystemMonitor:
    #Created Class Attribute for global control on time.sleep
    refresh_interval = 1.0

    #Gives Access to Classes Needed
    def __init__(self):
        self.running = True
        self.cpu = CPU()
        self.memory = Memory()
        self.drive = Drive()
    
    #Refreshes CPU and Memory for new Values per second
    def Monitoring(self):
            while self.running:
                self.cpu.update()
                self.memory.update()
                time.sleep(self.refresh_interval)

    #Runs Method from Drives Class to get drive data 
    def StaticInfo(self):
        self.drive.ScanD()
            
    #Displays SysMonitor
    def DisplayLayout(self):
        while self.running:
            #Refreshes Display 
            os.system("cls" if os.name == "nt" else "clear")

            print("----- SYSTEM MONITORING ACTIVE -----")
            print(f"CPU: {self.cpu.usage:5.1f}%")
            print(f"Memory Used: {self.memory.used_gb:6.2f} GB")
            print(f"Available: {self.memory.available_gb:6.2f} GB")
            print()
            print("----- DRIVES -----")
            for d in self.drive.DriveData:
                print(f"{d['name']} | Total: {round(d['total_gb'])} GB | Used: {round(d['used_gb'])} GB | Free: {round(d['free_gb'])} GB")


            time.sleep(self.refresh_interval)

    #Starts Methods and Processes for SysMonitor Class
    def run(self):
        try:      
            #Create the threads
            Monitoring_Thread = threading.Thread(target=self.Monitoring, daemon=True)
            Static_Thread = threading.Thread(target=self.StaticInfo)
            
            #Start the threads       
            Monitoring_Thread.start()
            Static_Thread.start()

            self.DisplayLayout()

            while self.running:
                time.sleep(self.refresh_interval)

            #Keep Main thread alive
            Static_Thread.join()

        except KeyboardInterrupt:
            self.running = False
            self.drive.DriveData.clear()
            print()
            time.sleep(0.2)
            print("Monitoring Stopped by User.")
            print()
            time.sleep(0.2)
               

    #Created Method to Test Parts of code
    def TestRun(self):
        pass


#Main = SystemMonitor()

#Main.run()