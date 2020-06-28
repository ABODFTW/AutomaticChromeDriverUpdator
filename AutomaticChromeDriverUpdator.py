import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import requests
from getFileProperties import *


"""
This Module will download and update Chrome driver without the client interaction, you just need to call update_driver() from your Selenium Script
"""


current_chrome_version = "current_chrome_version.txt"


def will_update(current_version):
    if os.path.isfile(current_chrome_version):
        latest_download = open(current_chrome_version, "r").read()[:2]
        if latest_download != current_version:
            return True
        else:
            print("Chrome driver is up to date.")
            return False
    else:
        return True

def update_driver():
    chrome_browser = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe' #-- ENTER YOUR Chrome.exe filepath

    cb_dictionary = getFileProperties(chrome_browser) # returns whole string of version (ie. 76.0.111)

    chrome_browser_version = cb_dictionary['FileVersion'][:2] # substring version to capabable version (ie. 77 / 76)
    
    if will_update(chrome_browser_version):
        print("Downloading Chrome Driver.")
        # Get versions from this link
        res = requests.get(f"https://chromedriver.storage.googleapis.com/?delimiter=/&prefix={chrome_browser_version}")

        root = ET.fromstring(res.content)

        vers = []
        for ele in root:
            for e in ele:
                vers.append(e.text)

        latest_chrome = vers[0]

        # Get the zip file from this link
        chrome_exe = requests.get(f"https://chromedriver.storage.googleapis.com/{latest_chrome}chromedriver_win32.zip")

        current_chrome_update = latest_chrome[0:-1]

        open(current_chrome_version, "w").write(current_chrome_update)

        with open("chromedriver_win32.zip", "wb") as f:
            f.write(chrome_exe.content)

        # Create a ZipFile Object and load sample.zip in it
        with ZipFile('chromedriver_win32.zip', 'r') as zipObj:
            # Extract all the contents of zip file in different directory
            zipObj.extractall()

        if os.path.isfile("chromedriver.exe"):
            print("Awesome!, Chromedriver have been downloaded")
        else:
            print("There is something wrong!")

        os.remove("chromedriver_win32.zip")
    else:
        pass


if __name__ == "__main__":
    update_driver()
