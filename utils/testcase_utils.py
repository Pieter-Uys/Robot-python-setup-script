import os
import subprocess
import logging
import sys
from colorama import Fore, Style

def create_dummy_testcase(project_dir, platform_name, platform_version, device_name, app_path, automation_name):
    dummy_test_case = f"""*** Settings ***
Library    AppiumLibrary

*** Variables ***
${{REMOTE_URL}}    http://localhost:4723/wd/hub
${{PLATFORM_NAME}}    {platform_name}
${{PLATFORM_VERSION}}    {platform_version}
${{DEVICE_NAME}}    {device_name}
${{APP_PATH}}    {app_path}
${{AUTOMATION_NAME}}    {automation_name}

*** Test Cases ***
Open Application
    Open Application    ${{REMOTE_URL}}    platformName=${{PLATFORM_NAME}}    platformVersion=${{PLATFORM_VERSION}}
    ...    deviceName=${{DEVICE_NAME}}    app=${{APP_PATH}}
    ...    automationName=${{AUTOMATION_NAME}}

Close Application
    Close Application
"""
    test_case_path = os.path.join(project_dir, "tests", "testcases", "dummy_test.robot")
    os.makedirs(os.path.dirname(test_case_path), exist_ok=True)
    with open(test_case_path, "w") as file:
        file.write(dummy_test_case)

def run_testcase(project_dir):
    test_case_path = os.path.join(project_dir, "tests", "testcases", "dummy_test.robot")
    print(f"{Fore.BLUE}Running the test case...{Style.RESET_ALL}")
    try:
        test_run_output = subprocess.check_output(["robot", test_case_path]).decode().strip()
        print(test_run_output)
        logging.info("Test case executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run the test case.{Style.RESET_ALL}")
        print(e.output.decode())
        logging.error("Failed to run the test case.")
        sys.exit(1)