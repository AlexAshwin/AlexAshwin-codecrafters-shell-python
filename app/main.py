import sys
import os

def handler_echo(args=None):
    if args.startswith('') and args.endswith(''):
        print(args.("'"))
    else:
        print(args if args else "")

def handler_exit(args=None):
    exit(0)

def handler_type(args):
    if args in builtin:
        print(f"{args} is a shell builtin")
    else:
        # Use os to check if the command is executable
        path = find_executable(args)
        if path:
            print(f"{args} is {path}")
        else:
            print(f"{args}: not found")

def find_executable(command):
    # Check if the command is in the system's PATH
    for dir in os.environ.get("PATH", "").split(os.pathsep):
        executable = os.path.join(dir, command)
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            return executable
    return None

def check_executable(args):
    script_path = find_executable(args.split()[0])
    if script_path:
        os.system(args)
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

# Define built-in handlers
builtin = {"echo": handler_echo, "exit": handler_exit, "type": handler_type, "pwd": handler_pwd, "cd": handler_change_directory}

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        parts = command.split(maxsplit=1)
        
        # If no arguments provided for commands like echo or type, pass None to the handler
        if len(parts) > 1:
            cmd, args = parts
        else:
            cmd, args = parts[0], None
        
        if cmd in builtin:
            builtin[cmd](args)
        else:
            check_executable(command)

if __name__ == "__main__":
    main()
