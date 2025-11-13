import os
import tempfile
import time
import shutil
from pathlib import Path

class tempCleaner:
    def __init__(self):
        self.tpath = tempfile.gettempdir() #Gets TEMP Env and has its Path
        

    def dry_run_check(self):
        self.dry_run = True
        dry_flag = True #While loop Flag (dry_run)

        while dry_flag:
            dry_run_choice = input("Run as Dry-Run (Y/N)?: ")
            time.sleep(0.1)
            print()
        
            if dry_run_choice.lower() in ("y", "yes"):
                self.dry_run = True #Testing mode
                dry_flag = False

            elif dry_run_choice.lower() in ("n", "no"):
                self.dry_run = False #Fully deletes Temp Files/Dirs
                dry_flag = False

            else:
                print("Select Y or N")
                print()
                time.sleep(0.1)
            
    def user_choice(self):
        other_flag = True
        self.deleted = 0
        self.skipped = 0
        self.files = 0
        self.folders = 0
        temp_dir = Path(self.tpath).resolve()

        while other_flag:
            choice = input("Do you want to clean these Temp files (Y/N)?: ")
            time.sleep(0.1)
            print()

            try:
                if choice.lower() in ("y", "yes"):
                    self.dry_run_check() #Dry run prompt

                    for d in os.listdir(temp_dir):
                        full_path = (Path(self.tpath) / d).resolve()

                        if temp_dir not in full_path.parents:
                            if not self.dry_run:
                                print(f"> Skipped suspicious path: {full_path}")
                                print()
                            else:
                                print(f"> [Dry-Run] would skip suspicious path: {d}")

                            time.sleep(0.1)
                            self.skipped += 1
                            continue

                        try:
                            if full_path.is_dir():
                                if not self.dry_run:
                                    shutil.rmtree(full_path)
                                    print(f"Deleted directory: {d}")
                                else:
                                    print(f"[Dry-Run] would delete directory: {d}")

                                time.sleep(0.1)
                                self.deleted += 1
                                self.folders += 1
                            
                            elif full_path.is_file():
                                if not self.dry_run:
                                    full_path.unlink()
                                    print(f"Deleted file: {d}")
                                else:
                                    print(f"[Dry-Run] would delete file: {d}")

                                time.sleep(0.1)
                                self.deleted += 1
                                self.files += 1

                            else:
                                print("> An issue accessing TEMP Dir")

                        except PermissionError:
                            print(f"> Skipped: {d}")
                            print()
                            time.sleep(0.1)
                            self.skipped += 1

                        except FileNotFoundError:
                            print(f"> {d} Already gone")
                            print()
                            time.sleep(0.1)
                            self.skipped += 1

                        except Exception as e:
                            print(f"> An issue with {d}: {e}")
                            print()
                            time.sleep(0.1)
                            self.skipped += 1

                elif choice.lower() in ("n", "no"):
                    pass

                else:
                    print("Select Y or N")
                    time.sleep(0.1)
                    print()
                    continue

                other_flag = False

            except Exception as e:
                print(f"An error happened: {e}")

    def Cleaner_Summarise(self):
        if not self.dry_run:
            print(f"> Deleted Directories: {self.folders}")
            time.sleep(0.1)
            print(f"> Deleted files: {self.files}")
            print()
            time.sleep(0.1)
            print(f"> Skipped entries: {self.skipped}")
            time.sleep(0.1)
            print(f"> {self.deleted} Entries have been deleted")
        else:
            print(f"> {self.folders} Directories would have been deleted")
            time.sleep(0.1)
            print(f"> {self.files} Files would have been deleted")
            print()
            time.sleep(0.1)
            print(f"> {self.skipped} Entries would have been skipped")
            time.sleep(0.1)
            print(f"> {self.deleted} Entries would have been deleted")
                    

    def display(self):
        print()
        print("----- Current Temp Files -----")
        print()
        time.sleep(0.1)
        print(f"> {self.tpath}")
        print()
        time.sleep(0.1)
        self.user_choice()
        print()
        time.sleep(0.1)
        print("----- Cleaner Summary -----")
        print()
        time.sleep(0.1)
        self.Cleaner_Summarise()
        print()



#Main = tempCleaner()

#Main.display()



