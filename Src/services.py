import subprocess
import json
import time
from pathlib import Path
from tabulate import tabulate



#Created Services Class. Later on give the option to scan critical services or net services
class Services:
    def __init__(self):
        self.services = []
        p = Path("config/service_categories.json")

        with open(p, "r") as f:
            self.categories = json.load(f)

    #Runs the Command to get Services for the parse method below
    def fetch_service(self):
        try:
            self.fetch = subprocess.run(["powershell", "-Command", "Get-CimInstance Win32_Service | Select Name, DisplayName, State, StartMode | ConvertTo-Json -Depth 3"], capture_output=True, text=True)
            if self.fetch.returncode == 0:
                self.raw_text = self.fetch.stdout
            else:
                print("An error happened")

        except FileNotFoundError:
            pass

    #Loads Fetch data as JSON then changes Status from Number Values to string Values "Stopped"
    def load_service(self):

        #Creates a list of Dicts
        services_data = json.loads(self.raw_text)
        net_stack = self.categories["network_stack"]["include"]
        crit_core = self.categories["critical_core"]["include"]
        rm_access = self.categories["remote_access"]["include"]
        self.check = True

        while self.check:
            self.choice = input("Select a category: ")

            try:
                if self.choice == "1":
                    for n in services_data:
                        for name in crit_core:
                            if n["Name"] == name:
                                self.services.append(n)
                                self.check = False

                elif self.choice == "2":
                    for n in services_data:
                        for name in net_stack:
                            if n["Name"] == name:
                                self.services.append(n)
                                self.check = False

                elif self.choice == "3":
                    for n in services_data:
                        for name in rm_access:
                            if n["Name"] == name:
                                self.services.append(n)
                                self.check = False

                else:
                    print()
                    print("Please try again")
                    print()
                    time.sleep(0.2)
                    continue
                    
            except TypeError:
                print()
                print("An error happened")
                print()
                time.sleep(0.2)
                continue



        




    #Displays Services using a for loop
    def displayService(self):
        print()
        print("1) Critical Core")
        print("2) Network Stack")
        print("3) Remote Access")
        print()
        time.sleep(0.2)
        self.load_service()
        print()

        print("--- Services ---")
        print()
        print(tabulate(self.services, headers="keys"))

        #Prevents the list from being cluttered during loop back of the Menu
        self.services.clear()
        print()
            

    
    def check_all_services(self):
        pass


Main = Services()

Main.fetch_service()
Main.displayService()