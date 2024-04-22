import subprocess
import sys
import logging
from colorama import Fore, Style

def check_android_studio_installation():
    try:
        android_studio_version = subprocess.check_output(["studio.bat", "--version"], shell=True).decode().strip()
        print(f"{Fore.GREEN}Android Studio version: {android_studio_version}{Style.RESET_ALL}")
        logging.info(f"Android Studio version: {android_studio_version}")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"{Fore.RED}Error: Android Studio is not installed or not found in the system's PATH.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please install Android Studio and ensure that the 'studio.bat' executable is available in the system's PATH.{Style.RESET_ALL}")
        logging.error("Android Studio is not installed or not found in the system's PATH.")
        sys.exit(1)

def check_adb_devices():
    try:
        adb_devices_output = subprocess.check_output(["adb", "devices"]).decode().strip()
        if "List of devices attached" in adb_devices_output:
            devices = adb_devices_output.split("\n")[1:]
            if len(devices) > 0:
                print(f"{Fore.GREEN}ADB devices are running:{Style.RESET_ALL}")
                for device in devices:
                    print(device)
                logging.info("ADB devices are running.")
            else:
                print(f"{Fore.RED}No ADB devices found. Please start an emulator or connect a physical device.{Style.RESET_ALL}")
                logging.error("No ADB devices found.")
                sys.exit(1)
        else:
            print(f"{Fore.RED}Error: Failed to retrieve ADB devices.{Style.RESET_ALL}")
            logging.error("Failed to retrieve ADB devices.")
            sys.exit(1)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"{Fore.RED}Error: ADB is not installed or not found in the system's PATH.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please ensure that you have the Android Debug Bridge (adb) installed and available in the system's PATH.{Style.RESET_ALL}")
        logging.error("ADB is not installed or not found in the system's PATH.")
        sys.exit(1)

def get_android_device_info():
    try:
        device_info = subprocess.check_output(["adb", "shell", "getprop"]).decode().strip().split("\n")
        platform_version = next(line.split(": ")[1] for line in device_info if line.startswith("ro.build.version.release"))
        device_name = next(line.split(": ")[1] for line in device_info if line.startswith("ro.product.model"))
        automation_name = "UIAutomator2"
        return platform_version, device_name, automation_name
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error: Failed to retrieve device information.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please ensure that you have the Android Debug Bridge (adb) installed and available in the system's PATH.{Style.RESET_ALL}")
        logging.error("Failed to retrieve device information.")
        sys.exit(1)