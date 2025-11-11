from Src.sysMonitor import SystemMonitor #SysMonitor Module
from Src.services import Services #Services Module
from Src.netdiag import Net_Diagnostic #Diagnostic Module
import time #Add pacing between code




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
                self.userSelect = input("Select a Number: ")
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
            print()
        elif self.choice in ("no", "n"):
            self.Flag = False
        else:
            print("Enter Y or N")
            print()
            time.sleep(0.2)
            

    #Stores a Check and runs Class Methods depending on user selection            
    def Menu_Check(self):
        if self.userConvert == 1:
            self.SystemMonitor.running = True
            self.SystemMonitor.run()
            

        elif self.userConvert == 2:
            self.Svc.fetch_service()
            self.Svc.displayService()
            print()

        elif self.userConvert == 3:
            self.NetDiag.fetch_Connection()
            self.NetDiag.pingConvert()
            print()

        else:
            print("Select a Valid Number")
            print()
            time.sleep(0.2)
            print()
            pass

          
#Run Script
Main = Menu()
Main.displayMenu()
print()
print("Script Finished")



