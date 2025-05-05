#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## ------ Imports ------ ##

import os
import sys
import subprocess
import time
import threading

## ------ Graphic designs ------ ##

# Colour codes
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'


def clear_screen():
    os.system('clear')

# Spinner animation
_spinner_running = False
_spinner_stop_event = threading.Event()

def _spin_cursor():
    # displays rotating ascii spinner
    global _spinner_running
    _spinner_running = True
    spinner_chars = ['[ | ]', '[ / ]', '[ - ]', '[ \\ ]']
    i = 0

    while not _spinner_stop_event.is_set():
        char = spinner_chars[i % len(spinner_chars)]
        sys.stdout.write(f'\rdetecting distro {char}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write('\r' + ' ' * (len("detecting distro") + 2) + '\r')
    sys.stdout.flush()
    _spinner_running = False

# Spinner animation
_spinner_2_running = False
_spinner_2_stop_event = threading.Event()

def _spin_cursor_2():
    # displays rotating ascii spinner
    global _spinner_2_running
    _spinner_2_running = True
    spinner_2_chars = ['[ | ]', '[ / ]', '[ - ]', '[ \\ ]']
    i = 0

    while not _spinner_2_stop_event.is_set():
        char = spinner_2_chars[i % len(spinner_2_chars)]
        sys.stdout.write(f'\rrefresh package lists {char}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write('\r' + ' ' * (len("refresh package lists") + 2) + '\r')
    sys.stdout.flush()
    _spinner_2_running = False


## ------ Productive code ------ ##

def detecting_distro():

    # Create variables
    distro_info = {
        "DISTRO_ID": "unknown",
        "DISTRO_NAME": "unknown",
        "DISTRO_VERSION": "unknown",
        "HAS_APT": False,
        "HAS_DNF": False,
        "HAS_ZYPPER_LEAP": False,
        "HAS_ZYPPER_TUMBLEWEED": False,
        "HAS_PACMAN": False,
        "HAS_YAY": False,
        "HAS_SNAP": False,
        "HAS_FLATPAK": False,
        "IS_UNKNOWN": True
    }

    # Detect path to bash script
    script_name = 'detect_distro.sh'
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    os.system('chmod +x detect_distro.sh')

    
    # Output error message if conditions are not fulfilled
    if not os.path.isfile(script_path):
        print(f"Error: Skript '{script_name}' could not be found.", file=sys.stderr)
        return None

    if not os.access(script_path, os.X_OK):
        print(f"Warning: Skript '{script_name}' is not executable.", file=sys.stderr)
        try:
            # Attempts to add rights
            os.chmod(script_path, os.stat(script_path).st_mode | 0o100)
            if not os.access(script_path, os.X_OK):
                 print(f"Error: Could not make '{script_name}' executable. Try it manually (`chmod +x {script_name}`).", file=sys.stderr)
                 return None
        except OSError as e:
            print(f"Error: {e}", file=sys.stderr)
            return None
    
    # Print text
    sys.stdout.write("detecting distro ")
    sys.stdout.flush()

    # Start Spinner in new Thread
    _spinner_stop_event.clear()
    spinner_thread = threading.Thread(target=_spin_cursor, daemon=True)
    spinner_thread.start()

    process_output = ""
    process_error = ""
    return_code = 1

    # Detect packet manager and distro
    try:
        # Execute bash script
        process = subprocess.run(
            [script_path],
            capture_output=True,
            text=True,
            check=False,
            timeout=10
        )
        process_output = process.stdout
        process_error = process.stderr
        return_code = process.returncode

    except FileNotFoundError:
        process_error = f"Error: script '{script_path}' not found"
        return_code = 127 # Exit-Code "command not found"
    except subprocess.TimeoutExpired:
         process_error = f"Fehler: Timeout ({process.timeout}s) in '{script_name}'"
         return_code = 124 # Exit-Code "timeout"
    except Exception as e:
        process_error = f"Error: '{script_name}': {e}"

    finally:
        # Stop Spinner
        _spinner_stop_event.set()
        spinner_thread.join(timeout=1)
        # Print green Message
        clear_screen()
        sys.stdout.write(f"\r{GREEN}detecting distro [ x ]{RESET}\n")
        sys.stdout.flush()


    if return_code != 0:
        print(f"Error: {script_name} (Exit Code: {return_code}):", file=sys.stderr)
        if process_error:
            print(process_error, file=sys.stderr)
        return distro_info

    # Processing the script output
    known_manager_found = False
    for line in process_output.strip().split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            if key in distro_info:
                # Turn Boolean-Strings to Python Booleans
                if value.lower() == 'true':
                    distro_info[key] = True
                    if key.startswith("HAS_"):
                        known_manager_found = True
                elif value.lower() == 'false':
                    distro_info[key] = False
                else:
                    # For non-boolean
                    distro_info[key] = value

    # Set HAS_UNKNOWN to False if at least one known manager was found
    if known_manager_found:
        distro_info["IS_UNKNOWN"] = False

    return distro_info


def program():
    clear_screen()
    print("--- This program runs in sudo mode ---")
    input("[ Press enter to start Update ]")
    clear_screen()

    ## ---- detecting_distro ---- ##
    detecting_distro()

    # Create variables
    detection_results = detecting_distro()

    has_apt = detection_results['HAS_APT']
    has_dnf = detection_results['HAS_DNF']
    has_zypper_leap = detection_results['HAS_ZYPPER_LEAP']
    has_zypper_tumbleweed = detection_results['HAS_ZYPPER_TUMBLEWEED']
    has_pacman = detection_results['HAS_PACMAN']
    has_yay = detection_results['HAS_YAY']
    has_snap = detection_results['HAS_SNAP']
    has_flatpak = detection_results['HAS_FLATPAK']
    distro_unknown = detection_results['IS_UNKNOWN']

    # Outputs results of package manager detection
    print("Detected package managers: ")

    if has_apt == True:
        print("apt")

    if has_dnf == True:
        print("dnf")

    if has_zypper_leap == True:
        print("Zypper - on openSUSE Leap")

    if has_zypper_tumbleweed == True:
        print("Zypper - on openSUSE Tumbleweed")

    if has_pacman == True:
        print("pacman")

    if has_yay == True:
        print("yay")

    if has_snap == True:
        print("snap - snapcraft")

    if has_flatpak == True:
        print("flatpak")

    if distro_unknown == True:
        print("\nNo package manager could be detected.")
        print(f"To use this program, a known package manager must be detected.\n")
        input("[ Press enter to exit program ]")
        sys.exit(1)

    ## ---- Refresh package lists ---- ##

    # Print text
    print("refresh package lists ", end='')
    sys.stdout.flush()
 
    # Start Spinner in new Thread
    _spinner_2_stop_event.clear()
    spinner_2_thread = threading.Thread(target=_spin_cursor_2, daemon=True)
    spinner_2_thread.start()

    process_output = ""
    process_error = ""
    return_code = 1
    
    # Refresh package lists
    if has_apt == True:
        script_name = 'refresh_repos/apt.sh'
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        os.system('chmod +x refresh_repos/apt.sh')

        subprocess.run([script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    if has_dnf == True:
        script_name = 'refresh_repos/dnf.sh'
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        os.system('chmod +x refresh_repos/dnf.sh')

        subprocess.run([script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    if has_zypper_leap == True:
        script_name = 'refresh_repos/zypper.sh'
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        os.system('chmod +x refresh_repos/zypper.sh')

        subprocess.run([script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    if has_zypper_tumbleweed == True:
        script_name = 'refresh_repos/zypper.sh'
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        os.system('chmod +x refresh_repos/zypper.sh')

        subprocess.run([script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    if has_pacman == True:
        script_name = 'refresh_repos/pacman.sh'
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        os.system('chmod +x refresh_repos/pacman.sh')

        subprocess.run([script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    if has_flatpak == True:
        script_name = 'refresh_repos/flatpak.sh'
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        os.system('chmod +x refresh_repos/flatpak.sh')

        subprocess.run([script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    
    # Stop Spinner
        _spinner_2_stop_event.set()
        spinner_2_thread.join(timeout=1)
        # Print green Message
        print(f"\r\r{GREEN}refresh package lists [ x ]{RESET}\n", end='')
        sys.stdout.flush()
    

    ## ---- Update Packages ---- ##

    # Write more code here



# Starts the program when it is executed with sudo permissions
def main():
    if os.geteuid() == 0:
        program()
    else:
        print("\nYou need to use this script in sudo mode.")
        print(f"Try run it again with: 'sudo update-linux'\n")
        input("[ Press enter to exit program ]")
        sys.exit(1)

if __name__ == "__main__":
    main()