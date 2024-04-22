import socket
import subprocess
import sys
import logging
import platform
from colorama import Fore, Style

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def check_appium_installation():
    try:
        # Detect the operating system
        os_type = platform.system()
        # Use 'appium.cmd' for Windows and 'appium' for others
        appium_command = "appium.cmd" if os_type == "Windows" else "appium"

        # Get the Appium version
        appium_version = subprocess.check_output([appium_command, "--version"], universal_newlines=True).strip()
        print(f"{Fore.GREEN}Appium version: {appium_version}{Style.RESET_ALL}")
        logging.info(f"Appium version: {appium_version}")
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"{Fore.RED}Error: Appium is not installed or not found in the system's PATH.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please install Appium and ensure that the Appium executable is available in the system's PATH.{Style.RESET_ALL}")
        logging.error(f"Appium is not installed or not found in the system's PATH: {e}")
        sys.exit(1)

def start_appium_server():
    appium_port = 4723  # default Appium port
    if is_port_in_use(appium_port):
        print(f"{Fore.YELLOW}Appium server already running on port {appium_port}{Style.RESET_ALL}")
        logging.info(f"Appium server already running on port {appium_port}")
        return
    
    try:
        # Construct the command to start Appium in a new terminal
        os_type = platform.system()
        if os_type == "Windows":
            appium_command = "start cmd /c appium"
        else:  # macOS, Linux, and other Unix-like systems
            appium_command = "osascript -e 'tell app \"Terminal\" to do script \"appium\"'"
        
        # Execute the command to start Appium in a new terminal
        subprocess.Popen(appium_command, shell=True)
        print(f"{Fore.BLUE}Appium server should now be starting in a new terminal window...{Style.RESET_ALL}")
        logging.info("Appium server command executed to open in a new terminal.")

    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred while trying to start Appium server: {e}{Style.RESET_ALL}")
        logging.error(f"An unexpected error occurred while trying to start Appium server: {e}")
        sys.exit(1)

