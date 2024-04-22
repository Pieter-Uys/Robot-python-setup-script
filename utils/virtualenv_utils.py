import os
import subprocess
import platform
import tqdm
import sys
from colorama import Fore, Style

def create_virtual_environment(venv_location, venv_name):
    venv_dir = os.path.join(venv_location, venv_name)
    print(f"{Fore.BLUE}Creating virtual environment at: {venv_dir}{Style.RESET_ALL}")
    subprocess.run([sys.executable, "-m", "venv", venv_dir])
    return venv_dir

def activate_virtual_environment(venv_dir):
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
        subprocess.run(activate_script, shell=True)
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")
        subprocess.run(["source", activate_script])

def install_required_packages_in_virtualenv():
    required_packages = ["robotframework-seleniumlibrary", 
                         "robotframework-jsonlibrary", 
                         "robotframework-requests",
                         "robotframework-appiumlibrary"]
    for package in tqdm.tqdm(required_packages, desc="Installing required packages", unit="package"):
        subprocess.run(["pip", "install", package])