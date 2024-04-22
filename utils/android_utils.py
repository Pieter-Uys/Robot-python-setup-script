import os
import subprocess
import sys
import platform
import logging
from colorama import Fore, Style

def check_android_studio_installation():
    os_type = platform.system()
    try:
        if os_type == "Windows":
            # Attempt to check the version using 'studio.bat' on Windows
            android_studio_version = subprocess.check_output(["studio.bat", "--version"], shell=True).decode().strip()
            print(f"{Fore.GREEN}Android Studio version: {android_studio_version}{Style.RESET_ALL}")
            logging.info(f"Android Studio version: {android_studio_version}")
        else:
            # For macOS and other systems, check for the presence of the application
            if os.path.exists("/Applications/Android Studio.app"):
                print(f"{Fore.GREEN}Android Studio is installed on macOS.{Style.RESET_ALL}")
                logging.info("Android Studio is installed on macOS.")
            else:
                raise FileNotFoundError
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"{Fore.RED}Error: Android Studio is not installed or not found.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please install Android Studio. Visit https://developer.android.com/studio/install{Style.RESET_ALL}")
        logging.error("Android Studio is not installed or not found.")
        sys.exit(1)

def check_adb_devices():
    try:
        adb_devices_output = subprocess.check_output(["adb", "devices"], universal_newlines=True).decode().strip()
        if "List of devices attached" in adb_devices_output:
            devices = adb_devices_output.split("\n")[1:]
            if any(device.strip() for device in devices):
                print(f"{Fore.GREEN}ADB devices are running:{Style.RESET_ALL}")
                for device in devices:
                    print(device)
                logging.info("ADB devices are running.")
            else:
                print(f"{Fore.RED}No ADB devices found. Starting an emulator...{Style.RESET_ALL}")
                logging.error("No ADB devices found.")
        else:
            print(f"{Fore.RED}Error: Failed to retrieve ADB devices.{Style.RESET_ALL}")
            logging.error("Failed to retrieve ADB devices.")
            sys.exit(1)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: ADB is not installed or not found in the system's PATH.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please ensure that you have the Android Debug Bridge (adb) installed and available in the system's PATH.{Style.RESET_ALL}")
        logging.error("ADB is not installed or not found in the system's PATH.")
        sys.exit(1)

def get_android_device_info():
    try:
        device_info = subprocess.check_output(["adb", "shell", "getprop"], universal_newlines=True).strip().split("\n")
        platform_version = next((line.split(": ")[1].strip() for line in device_info if "ro.build.version.release" in line), None)
        device_name = next((line.split(": ")[1].strip() for line in device_info if "ro.product.model" in line), None)
        automation_name = "UIAutomator2"

        if not platform_version or not device_name:
            raise ValueError("Device information incomplete.")

        return platform_version, device_name, automation_name
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"{Fore.RED}Error: Failed to retrieve device information. {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please ensure that you have the Android Debug Bridge (adb) installed and available in the system's PATH.{Style.RESET_ALL}")
        logging.error("Failed to retrieve device information.")
        sys.exit(1)
