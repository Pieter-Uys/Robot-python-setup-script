import os
import subprocess
import platform
import logging
from colorama import Fore, Style

def command_exists(command):
    """Check if a command exists on system path"""
    try:
        subprocess.check_output(['where' if os.name == 'nt' else 'which', command])
        return True
    except subprocess.CalledProcessError:
        return False

def check_android_studio_installation():
    studio_path_windows = "C:\\Program Files\\Android\\Android Studio"
    studio_path_mac = "/Applications/Android Studio.app"
    os_type = platform.system()
    if os_type == "Windows" and os.path.isdir(studio_path_windows):
        print(f"{Fore.GREEN}Android Studio is installed on Windows.{Style.RESET_ALL}")
        logging.info("Android Studio is installed on Windows.")
    elif os_type == "Darwin" and os.path.isdir(studio_path_mac):
        print(f"{Fore.GREEN}Android Studio is installed on macOS.{Style.RESET_ALL}")
        logging.info("Android Studio is installed on macOS.")
    else:
        print(f"{Fore.RED}Error: Android Studio is not installed or not found.{Style.RESET_ALL}")
        logging.error("Android Studio is not installed or not found.")
        print(f"{Fore.YELLOW}Please install Android Studio. Visit https://developer.android.com/studio/install{Style.RESET_ALL}")
        raise EnvironmentError("Android Studio is not installed or not found.")

def start_first_available_emulator():
    if not command_exists("emulator"):
        logging.error("Emulator command is not found in your system's PATH.")
        raise EnvironmentError("Emulator command is not found in your system's PATH.")

    avd_list_output = subprocess.check_output(["emulator", "-list-avds"], universal_newlines=True).strip()
    avds = avd_list_output.splitlines()
    if avds:
        avd_name = avds[0]
        subprocess.Popen(["emulator", "-avd", avd_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Emulator {avd_name} started.")
    else:
        raise EnvironmentError("No available AVDs to start.")

def check_adb_devices():
    if not command_exists("adb"):
        logging.error("ADB command is not found in your system's PATH.")
        raise EnvironmentError("ADB command is not found in your system's PATH.")

    adb_devices_output = subprocess.check_output(["adb", "devices"], universal_newlines=True).strip()
    if "List of devices attached" in adb_devices_output:
        devices = adb_devices_output.split("\n")[1:]
        devices = [device for device in devices if device.strip()]  # Remove empty lines
        if not devices:
            start_first_available_emulator()
    else:
        logging.error("Failed to retrieve ADB devices.")
        raise EnvironmentError("Failed to retrieve ADB devices.")

def get_android_device_info():
    device_info = subprocess.check_output(["adb", "shell", "getprop"], universal_newlines=True).strip().split("\n")
    platform_version = next((line.split(": ")[1].strip() for line in device_info if "ro.build.version.release" in line), None)
    device_name = next((line.split(": ")[1].strip() for line in device_info if "ro.product.model" in line), None)
    automation_name = "UIAutomator2"
    if not platform_version or not device_name:
        logging.error("Failed to retrieve device information.")
        raise ValueError("Device information incomplete.")
    return platform_version, device_name, automation_name
