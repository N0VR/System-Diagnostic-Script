import subprocess
import json
import time



#Created Services Class. Later on give the option to scan critical services or net services
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
            print(f"{svc['DisplayName']} - {svc['Status']}")
            time.sleep(0.2)

        #Prevents the list from being cluttered during loop back of the Menu
        self.services.clear()
            

    
    def check_all_services(self):
        pass


#Main = Services()

#Main.fetch_service()
#Main.load_service()
#Main.displayService()