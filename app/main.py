import sys
import os
import subprocess

def handler_echo(args=None):
    if ("1>" in args):
        args = args.split(" 1> ")
        args[0] = args[0].strip("'")
        with open(args[1], 'w') as f:
            f.write(args[0])

    elif (">" in args):
        args = args.split(" > ")
        args[0] = args[0].strip("'")
        with open(args[1], 'w') as f:
            f.write(args[0])

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
    sys.stdout.write("$ ")

def find_executable(command):
    for dir in os.environ.get("PATH", "").split(os.pathsep):
        executable = os.path.join(dir, command)
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            return executable
    return None

def check_executable(args):
    script_path = find_executable(args.split()[0])
    if script_path:
        # Check if the command contains the '>' operator
        if '>' in args:
            command, file_name = args.split('>', 1)
            file_name = file_name.strip()
            with open(file_name, 'w') as f:
                subprocess.run(command, shell=True, stdout=f)
            return
        subprocess.run(args, shell=True)
    else:
        print(f"{args}: not found")
    sys.stdout.write("$ ")

def handler_pwd(args=None):
    print(os.getcwd())
    sys.stdout.write("$ ")

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
    sys.stdout.write("$ ")

def handler_cat(args):
    try:
        with open(args, 'r') as f:
            sys.stdout.write(f.read())
    except FileNotFoundError:
        print(f"cat: {args}: No such file or directory")

builtin = {"echo": handler_echo, "exit": handler_exit, "type": handler_type, "pwd": handler_pwd, "cd": handler_change_directory, "cat": handler_cat}

def main():
    while True:
        sys.stdout.write("$ ")
        command = input().strip()

        if not command:
            continue

        parts = command.split(maxsplit=1)
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
