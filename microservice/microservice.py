# In this file, we define two endpoints: /installed_programs and /uninstall_programs.
# The installed_programs endpoint returns a list of installed programs. We use the psutil library to get a list of
# running processes, filter out any non-application processes, and return the list of installed programs as a JSON response.
# The /uninstall_programs endpoint receives a list of programs to uninstall as a JSON payload. It then iterates over
# the list of programs, executes the appropriate uninstall command, and returns a JSON response containing the results
# of each uninstall attempt.
# Please keep in mind that this example uses subprocess to execute uninstall commands, which can be
# potentially dangerous if not properly sanitized.

from flask import Flask, jsonify, request
import os
import platform
import winreg
import re
import subprocess

app = Flask(__name__)


@app.route('/installed_programs', methods=['GET'])
def get_installed_programs():
    installed_programs = []

    if platform.system() == 'Windows':
        registry_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'),
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'),
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
        ]

        for registry_key, subkey_path in registry_keys:
            try:
                hkey = winreg.OpenKey(registry_key, subkey_path)
            except FileNotFoundError:
                continue

            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(hkey, i)
                    subkey = winreg.OpenKey(hkey, subkey_name)
                    display_name, _ = winreg.QueryValueEx(subkey, 'DisplayName')
                    installed_programs.append(display_name)
                    i += 1
                except (OSError, FileNotFoundError):
                    break

        # Check the 'Program Files' and 'Program Files (x86)' directories
        program_files_dirs = [os.environ['ProgramFiles'], os.environ['ProgramFiles(x86)']]
        for program_files_dir in program_files_dirs:
            if os.path.exists(program_files_dir):
                installed_programs.extend(os.listdir(program_files_dir))

    installed_programs = list(set(installed_programs))
    installed_programs.sort()  # Sort the list in alphabetical order
    return jsonify(installed_programs=installed_programs)

@app.route('/uninstall_programs', methods=['POST'])
def uninstall_programs():
    programs_to_uninstall = request.json['programs_to_uninstall']
    uninstall_results = {}
    for program in programs_to_uninstall:
        try:
            uninstall_string = get_uninstall_string(program)
            if uninstall_string:
                subprocess.run(uninstall_string, shell=True, check=True)
                uninstall_results[program] = 'Uninstalled successfully'
            else:
                uninstall_results[program] = 'Failed to find uninstall string'
        except Exception as e:
            # Handle errors and provide detailed error messages
            uninstall_results[program] = f'Failed to uninstall: {str(e)}'
    # Refresh list of installed programs after uninstallation
    installed_programs = get_installed_programs().get_json()['installed_programs']
    return jsonify(uninstall_results=uninstall_results)

def get_uninstall_string(program_name):
    registry_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'),
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'),
        (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
    ]

    program_name_pattern = re.compile(re.escape(program_name), re.IGNORECASE)

    for registry_key, subkey_path in registry_keys:
        try:
            hkey = winreg.OpenKey(registry_key, subkey_path)
        except FileNotFoundError:
            continue

        i = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(hkey, i)
                subkey = winreg.OpenKey(hkey, subkey_name)
                display_name, _ = winreg.QueryValueEx(subkey, 'DisplayName')
                if display_name and program_name_pattern.search(display_name):
                    uninstall_string, _ = winreg.QueryValueEx(subkey, 'UninstallString')
                    return uninstall_string
                i += 1
            except (OSError, FileNotFoundError):
                break
    return None


if __name__ == '__main__':
    app.run(debug=True)
