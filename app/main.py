import sys
import os
import shlex

def handler_echo(args=None, redirect_file=None):
    if args:
        # Split like a shell would, preserving quoted spaces and handling escapes
        parsed_args = shlex.split(args, posix=True)
        # Join and print the args, redirect to file if needed
        output = " ".join(parsed_args)
        if redirect_file:
            with open(redirect_file, 'w') as f:
                f.write(output + "\n")
        else:
            print(output)
    else:
        print("")

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

def find_executable(command):
    for dir in os.environ.get("PATH", "").split(os.pathsep):
        executable = os.path.join(dir, command)
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            return executable
    return None

def check_executable(command, redirect_file=None):
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

def handler_pwd(args=None, redirect_file=None):
    output = os.getcwd()
    if redirect_file:
        with open(redirect_file, 'w') as f:
            f.write(output + "\n")
    else:
        print(output)

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

builtin = {
    "echo": handler_echo,
    "exit": handler_exit,
    "type": handler_type,
    "pwd": handler_pwd,
    "cd": handler_change_directory
}

def parse_redirect(command):
    # Check if there's a redirection operator (> or 1>)
    if ">" in command:
        parts = command.split(">")
        cmd = parts[0].strip()  # The actual command
        file_name = parts[1].strip()  # The file to redirect output to
        return cmd, file_name
    return command, None

def main():
    while True:
        print("$ ", end="", flush=True)
        command = input()

        if not command.strip():
            continue

        # Check for redirection operator
        command, redirect_file = parse_redirect(command)

        try:
            parts = shlex.split(command)
        except ValueError as e:
            print(f"Error parsing command: {e}")
            continue

        cmd = parts[0]
        args = " ".join(parts[1:]) if len(parts) > 1 else None

        if cmd in builtin:
            builtin[cmd](args, redirect_file)
        else:
            check_executable(command, redirect_file)

if __name__ == "__main__":
    main()
