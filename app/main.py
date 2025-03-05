import sys
import os
import shlex

# Handler functions for built-in commands
def handler_echo(args=None, redirect=False, file_path=None):
    if redirect:
        with open(file_path, 'w') as f:
            f.write(args + "\n")
    else:
        print(args)

def handler_exit(args=None):
    exit(0)

def handler_type(args):
    if args in builtin:
        print(f"{args} is a shell builtin")
    else:
        path = find_executable(args)
        if path:
            print(f"{args} is {path}")
        else:
            print(f"{args}: not found")

def handler_pwd(args=None):
    print(os.getcwd())

def handler_change_directory(args):
    if args == '~':
        os.chdir(os.path.expanduser('~'))
    elif args == '/':
        os.chdir('/')
    else:
        try:
            os.chdir(args)
        except FileNotFoundError:
            print(f"cd: {args}: No such file or directory")

# Find the executable in the system's PATH
def find_executable(command):
    for dir in os.environ.get("PATH", "").split(os.pathsep):
        executable = os.path.join(dir, command)
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            return executable
    return None

# Execute non-built-in commands with redirection
def check_executable_with_redirection(command, file_path):
    try:
        parts = shlex.split(command)
    except ValueError as e:
        print(f"Error parsing command: {e}")
        return

    script_path = find_executable(parts[0])
    if script_path:
        # Redirect the output to the specified file
        with open(file_path, 'w') as f:
            sys.stdout = f  # Redirect stdout to file
            os.system(command)
            sys.stdout = sys.__stdout__  # Reset stdout back to terminal
    else:
        print(f"{parts[0]}: not found")

# Check for executable command (non-built-in)
def check_executable(command):
    try:
        parts = shlex.split(command)
    except ValueError as e:
        print(f"Error parsing command: {e}")
        return

    script_path = find_executable(parts[0])
    if script_path:
        os.system(command)
    else:
        print(f"{parts[0]}: not found")

# Handle redirection and built-in command execution
def main():
    while True:
        print("$ ", end="", flush=True)
        command = input()

        if not command.strip():
            continue

        # Handle redirection (1> or >)
        if '>' in command:
            parts = command.split('>')
            cmd_part = parts[0].strip()
            file_path = parts[1].strip()

            # Find the command and its arguments
            try:
                parts = shlex.split(cmd_part)
            except ValueError as e:
                print(f"Error parsing command: {e}")
                continue

            cmd = parts[0]
            args = " ".join(parts[1:]) if len(parts) > 1 else None

            # Redirect output to the file
            if cmd in builtin:
                if args:
                    with open(file_path, 'w') as f:
                        sys.stdout = f  # Redirect stdout to file
                        builtin[cmd](args)
                        sys.stdout = sys.__stdout__  # Reset stdout back to terminal
                else:
                    with open(file_path, 'w') as f:
                        sys.stdout = f
                        builtin[cmd](args)
                        sys.stdout = sys.__stdout
