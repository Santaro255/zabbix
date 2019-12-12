import os

list_files = os.listdir()

for i in list_files:
    if i.endswith(".py"):
        if "scan_devices_" in i:
            os.startfile(i)
