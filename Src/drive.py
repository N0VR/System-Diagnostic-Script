import psutil




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