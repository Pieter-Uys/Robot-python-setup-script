import os
import sys
import subprocess
import yaml
import tkinter as tk
from tkinter import filedialog
from colorama import init, Fore, Style
from utils import setup_utils, logging_utils, virtualenv_utils, appium_utils, android_utils, ios_utils, web_utils, testcase_utils
from utils.loader import Loader

# Initialize colorama
init()

# Install required packages from requirements.txt
with Loader("Installing required packages...", color=Fore.CYAN):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Load configuration from YAML file
config = setup_utils.load_config("config.yaml")

# Set up logging
logging_utils.configure_logging()

# Install required packages
setup_utils.install_required_packages()

# Create project directory
project_dir = setup_utils.create_project_directory(config)

# Prompt the user for the virtual environment location
print(f"{Fore.BLUE}Select the location to create the virtual environment:{Style.RESET_ALL}")
root = tk.Tk()
root.withdraw()
venv_location = filedialog.askdirectory(title="Select Virtual Environment Location")

# Prompt the user for the virtual environment name
venv_name = input(f"{Fore.BLUE}Enter the name for the virtual environment: {Style.RESET_ALL}")

# Create and activate virtual environment
with Loader(f"Creating virtual environment '{venv_name}'...", color=Fore.MAGENTA):
    venv_dir = virtualenv_utils.create_virtual_environment(venv_location, venv_name)
    virtualenv_utils.activate_virtual_environment(venv_dir)

# Install required packages in the virtual environment
with Loader("Installing packages in the virtual environment...", color=Fore.CYAN):
    virtualenv_utils.install_required_packages_in_virtualenv()

# Check Appium installation and start Appium server
with Loader("Checking Appium installation...", color=Fore.YELLOW):
    appium_utils.check_appium_installation()
with Loader("Starting Appium server...", color=Fore.YELLOW):
    appium_utils.start_appium_server()

# Get platform from configuration or user input
platform_name = setup_utils.get_platform(config)

if platform_name == "Android":
    android_utils.check_android_studio_installation()
    android_utils.check_adb_devices()
    platform_version, device_name, automation_name = android_utils.get_android_device_info()
elif platform_name == "iOS":
    platform_version, device_name, automation_name = ios_utils.get_ios_device_info()
else:
    platform_version, device_name, automation_name = web_utils.get_web_browser_info()

# Get app path from configuration or user input
app_path = setup_utils.get_app_path(config, project_dir)

# Create dummy test case
testcase_utils.create_dummy_testcase(project_dir, platform_name, platform_version, device_name, app_path, automation_name)

# Run the test case
with Loader("Running the test case...", color=Fore.MAGENTA):
    testcase_utils.run_testcase(project_dir)

print(f"{Fore.GREEN}Project '{config['project_name']}' has been set up successfully!{Style.RESET_ALL}")
print(f"{Fore.BLUE}The virtual environment '{venv_name}' is still active.{Style.RESET_ALL}")