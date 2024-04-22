import subprocess
import sys
import logging
import platform
from colorama import Fore, Style
import os

print("PATH !!!!", os.environ['PATH'])

def check_appium_installation():
    try:
        appium_version = subprocess.check_output(["appium", "--version"]).decode().strip()
        print(f"{Fore.GREEN}Appium version: {appium_version}{Style.RESET_ALL}")
        logging.info(f"Appium version: {appium_version}")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"{Fore.RED}Error: Appium is not installed or not found in the system's PATH.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please install Appium and ensure that the Appium executable is available in the system's PATH.{Style.RESET_ALL}")
        logging.error("Appium is not installed or not found in the system's PATH.")
        sys.exit(1)

def start_appium_server():
    try:
        appium_path = subprocess.check_output(["where" if platform.system() == "Windows" else "which", "appium"]).decode().strip().splitlines()[0]
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error: Failed to find the Appium executable path.{Style.RESET_ALL}")
        logging.error("Failed to find the Appium executable path.")
        sys.exit(1)
    print(f"{Fore.BLUE}Starting Appium server...{Style.RESET_ALL}")
    appium_process = subprocess.Popen([appium_path])