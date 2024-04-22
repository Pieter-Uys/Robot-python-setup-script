import os
import sys
import yaml
import subprocess
import shutil
from colorama import Fore, Style

def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return yaml.safe_load(file)
    else:
        return {}

def install_required_packages():
    packages_to_install = ["tqdm", "psutil", "colorama", "pyyaml"]
    for package in packages_to_install:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package} library...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installation completed.")

def create_project_directory(config):
    project_name = config.get("project_name", "")
    while not project_name:
        project_name = input(f"{Fore.BLUE}Enter your project name: {Style.RESET_ALL}")
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir, exist_ok=True)
    return project_dir

def get_platform(config):
    platforms = ["Android", "iOS", "Web"]
    platform_name = config.get("platform", "")
    while platform_name not in platforms:
        print(f"{Fore.BLUE}Select the platform:{Style.RESET_ALL}")
        for i, platform in enumerate(platforms, start=1):
            print(f"{i}. {platform}")
        choice = input(f"{Fore.BLUE}Enter your choice (1-{len(platforms)}): {Style.RESET_ALL}")
        try:
            index = int(choice) - 1
            if 0 <= index < len(platforms):
                platform_name = platforms[index]
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid choice. Please enter a number.{Style.RESET_ALL}")
    return platform_name

def get_app_path(config, project_dir):
    app_path = config.get("app_path", "")
    while not app_path or not os.path.exists(app_path):
        app_path = input(f"{Fore.BLUE}Enter the path to the app file: {Style.RESET_ALL}")
    app_folder = os.path.join(project_dir, "app")
    os.makedirs(app_folder, exist_ok=True)
    shutil.copy(app_path, app_folder)
    return os.path.join(app_folder, os.path.basename(app_path))