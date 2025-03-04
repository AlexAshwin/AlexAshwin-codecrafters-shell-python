import shutil
import sys
import os

def handler_echo(args):
    print(args)

def handler_exit():
    exit(0)

def handler_type(args,builtin):
    if args in builtin:
        print(f"{args} is a shell builtin")
    else:
        path = shutil.which(args)
        if path:
            print(f"{args} is {path}")
        else:
            print(f"{args}: not found")

def check_executable(args=None):

    script_path = shutil.which(args.split()[0])
    if script_path:
        os.system(args)
    else:
        print(f"{args}: not found")

builtin = {"echo": handler_echo, "exit": handler_exit, "type": handler_type}

def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        command = input()
        if command.split()[0] in builtin:
            builtin[command.split()[0]](command.split()[1:],builtin)
        else:
            check_executable(command)

if __name__ == "__main__":
    main()