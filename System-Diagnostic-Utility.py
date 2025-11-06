import psutil #Hardware Monitoring
import os, shutil, tempfile #File System and Cleanup Operations
import subprocess #Checks Windows service states
import platform #Determines system's OS for ping commands
import datetime #Timestamp reports and logs
import time #Add pacing between code
import threading
import json

#Creating CPU Class
class CPU:
    def __init__(self):
        self.usage = 0.0
        psutil.cpu_percent(interval=None)

    def update(self):
        self.usage = psutil.cpu_percent(interval=0)

#Creating Memory Class
class Memory:
    def __init__(self):
        pass

    def update(self):
        mem = psutil.virtual_memory()
        self.used_gb = mem.used / (1024 ** 3)
        self.available_gb = mem.available / (1024 ** 3)

#Creating Drive class
class Drive:
    def __init__(self):
        self.DriveData = []

    def ScanD(self):
        for d in psutil.disk_partitions():
            try:
                if d.fstype == "NTFS":
                    usage = psutil.disk_usage(d.device)

                    drive_info = {
                        "name": d.device,
                        "total_gb": usage.total / (1024 ** 3),
                        "used_gb": usage.used / (1024 ** 3),
                        "free_gb": usage.free / (1024 ** 3),
                        "percent": usage.percent
                    }

                    self.DriveData.append(drive_info)
            except PermissionError:
                continue

class Services:
    def __init__(self):
        self.services = []

    def fetch_service(self):
        try:
            self.fetch = subprocess.run(["powershell", "-Command", "Get-Service", "-Name", "win*", "|", "Select-Object", "Name," "DisplayName,", "Status", "|", "ConvertTo-Json"], capture_output=True, text=True)
            if self.fetch.returncode == 0:
                self.raw_text = self.fetch.stdout
            else:
                print("An error happened")

        except FileNotFoundError:
            pass

    def parse_service(self):
        status_Map = {1: "Stopped", 2: "StartPending", 3: "StopPending", 4: "Running", 5: "ContinuePending", 6: "PausePending", 7: "Paused"}
        services_data = json.loads(self.raw_text)

        for svc in services_data:
            name = svc["Name"]
            displayname = svc["DisplayName"]
            status = svc["Status"]

            if status in status_Map:
                svc["Status"] = status_Map[status]
            else:
                svc["Status"] = "Unknown"

            self.services.append(svc)


    def displayService(self):
        print("--- Services ---")

        for svc in self.services:
            print(f"{svc['Name']} - {svc['Status']}")
            time.sleep(0.2)

        self.services.clear()
            

        

    def check_all_services(self):
        pass


#Creating SystemMonitor Class / Main
class SystemMonitor:
    refresh_interval = 1.0

    def __init__(self):
        self.running = True
        self.cpu = CPU()
        self.memory = Memory()
        self.drive = Drive()

    def Monitoring(self):
            while self.running:
                self.cpu.update()
                self.memory.update()
                time.sleep(self.refresh_interval)

    
    def StaticInfo(self):
        self.drive.ScanD()
            

    def DisplayLayout(self):
        while self.running:
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
            print()
            time.sleep(0.2)
            print("Monitoring Stopped by User.")
            print()
            time.sleep(0.2)
               

        
    def TestRun(self):
        self.service = Services()

        self.service.fetch_service()
        self.service.parse_service()
        self.service.displayService()
        print()
        time.sleep(0.5)

class Menu:
    Flag = True

    def __init__(self):
        self.SystemMonitor = SystemMonitor()
        self.Svc = Services()

    def displayMenu(self):
        while self.Flag:
            print("--- System Diagnostic Utility 1.0 ---")
            time.sleep(0.2)
            print()
            print("1) Real Time Monitor")
            print("2) Display Services")
            print()
            time.sleep(0.2)

            try:
                self.userSelect = input("Select One or Two: ")
                self.userConvert = int(self.userSelect)
                time.sleep(0.2)
                print()
                
            except ValueError:
                print()
                print("Please Select a Number.")
                continue

            self.Menu_Check()

            self.UserMenu = input("Go back to Menu (Y/N)?: ")
            self.choice = self.UserMenu.lower()

            self.Menu_Return()


    def Menu_Return(self):
        if self.choice in ("yes", "y"):
            pass
        elif self.choice in ("no", "n"):
            self.Flag = False
            

            

                
    def Menu_Check(self):
        if self.userConvert == 1:
            pass
            print()
        elif self.userConvert == 2:
            self.Svc.fetch_service()
            self.Svc.parse_service()
            self.Svc.displayService()
            print()

            

#Run Script
Main = Menu()
#Main.run()
Main.displayMenu()
print()
print("Script Finished")



