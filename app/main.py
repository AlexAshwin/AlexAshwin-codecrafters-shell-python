import sys
import os
import shlex

def handler_echo(args=None):
    if args:
        # Split like a shell would, preserving quoted spaces
        parsed_args = shlex.split(args)
        print(" ".join(parsed_args))
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

builtin = {
    "echo": handler_echo,
    "exit": handler_exit,
    "type": handler_type,
    "pwd": handler_pwd,
    "cd": handler_change_directory
}

def main():
    while True:
        print("$ ", end="", flush=True)
        command = input()

        if not command.strip():
            continue

        try:
            parts = shlex.split(command)
        except ValueError as e:
            print(f"Error parsing command: {e}")
            continue

        cmd = parts[0]
        args = " ".join(parts[1:]) if len(parts) > 1 else None

        if cmd in builtin:
            builtin[cmd](args)
        else:
            check_executable(command)

if __name__ == "__main__":
    main()
