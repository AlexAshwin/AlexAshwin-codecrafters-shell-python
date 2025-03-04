import shutil
import sys
import os


def handler_echo(args):
    print(args)

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

    script_path = shutil.which(args.split()[0])
    if script_path:
        os.system(args)
    else:
        print(f"{args}: not found")

def handler_pwd(args=None):
    print(os.getcwd())

builtin = {"echo": handler_echo, "exit": handler_exit, "type": handler_type ,"pwd": handler_pwd}

def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        command = input()
        if command.split()[0] in builtin:
            builtin[command.split()[0]](command.split(maxsplit=1)[1])
        else:
            check_executable(command)

if __name__ == "__main__":
    main()