import subprocess
import json




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


#Main = Net_Diagnostic()

#Main.fetch_Connection()
#Main.pingConvert()