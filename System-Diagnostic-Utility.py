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

    #Convert Mem to GB
    def update(self):
        mem = psutil.virtual_memory()
        self.used_gb = mem.used / (1024 ** 3)
        self.available_gb = mem.available / (1024 ** 3)

#Creating Drive class
class Drive:
    def __init__(self):
        #Empty list for storing Drives
        self.DriveData = []

    #Scans for NTFS drives and converts disk space to GB
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

    #Runs the Command to get Services for the parse method below
    def fetch_service(self):
        try:
            self.fetch = subprocess.run(["powershell", "-Command", "Get-Service", "-Name", "win*", "|", "Select-Object", "Name," "DisplayName,", "Status", "|", "ConvertTo-Json"], capture_output=True, text=True)
            if self.fetch.returncode == 0:
                self.raw_text = self.fetch.stdout
            else:
                print("An error happened")

        except FileNotFoundError:
            pass

    #Loads Fetch data as JSON then changes Status from Number Values to string Values "Stopped"
    def load_service(self):

        #Used to make the status user friendly
        status_Map = {1: "Stopped", 2: "StartPending", 3: "StopPending", 4: "Running", 5: "ContinuePending", 6: "PausePending", 7: "Paused"}

        #Creates a list of Dicts
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

    #Displays Services using a for loop
    def displayService(self):
        print("--- Services ---")

        for svc in self.services:
            print(f"{svc['Name']} - {svc['Status']}")
            time.sleep(0.2)

        #Prevents the list from being cluttered during loop back of the Menu
        self.services.clear()
            

    
    def check_all_services(self):
        pass


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
        self.NetD = Net_Diagnostic()
        self.NetD.fetch_Connection()

        print(json.loads(self.NetD.pingRaw))


        time.sleep(0.5)


class Net_Diagnostic:
    def __init__(self):
        pass

    def fetch_Connection(self):
        self.ping = subprocess.run(["powershell", "-Command", "test-connection", "8.8.8.8", "-count", "3", "|", "ConvertTo-Json"], capture_output=True, text=True)
        self.pingRaw = self.ping.stdout

    def pingConvert(self):
        ping_data = json.loads(self.pingRaw)
        result = ping_data[0]
        
        print("--- Network Test --- ")
        if result['StatusCode'] == 0:
            print(f"Target: {result['Address']}")
            print(f"Status: ONLINE")
            print(f"Latency: {result['ResponseTime']}ms")

        else:
            print(f"Target: {result['Address']}")
            print(f"Status: OFFLINE")
            print("Check your network connection.")


#Created Main Menu Class
class Menu:
    Flag = True
    
    #Feed SysMonitor and Services Class into Main Menu
    def __init__(self):
        self.SystemMonitor = SystemMonitor()
        self.Svc = Services()
        self.NetDiag = Net_Diagnostic()

    #Visual Display of Menu
    def displayMenu(self):

        #Used While loop to loop back to main menu
        while self.Flag:
            print("--- System Diagnostic Utility 1.0 ---")
            time.sleep(0.2)
            print()
            print("1) Real Time Monitor")
            print("2) Display Services")
            print("3) Ping")
            print()
            time.sleep(0.2)

            #Check User Input is Correct with try and except block
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

    #Stores a Check to see if user wants to loop back or quit
    def Menu_Return(self):
        if self.choice in ("yes", "y"):
            pass
        elif self.choice in ("no", "n"):
            self.Flag = False

    #Stores a Check and runs Class Methods depending on user selection            
    def Menu_Check(self):
        if self.userConvert == 1:
            self.SystemMonitor.running = True
            self.SystemMonitor.run()
            print()

        elif self.userConvert == 2:
            self.Svc.fetch_service()
            self.Svc.load_service()
            self.Svc.displayService()
            print()

        elif self.userConvert == 3:
            self.NetDiag.fetch_Connection()
            self.NetDiag.pingConvert()
            print()

        else:
            print("Select One or Two")
            print()
            time.sleep(0.2)
            print()
            pass

          
#Run Script
Main = Menu()
Main.displayMenu()
print()
print("Script Finished")



