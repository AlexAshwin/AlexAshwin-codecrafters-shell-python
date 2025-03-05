import sys
import os
import subprocess

def handler_echo(args=None):
    if args is None:
        return

    # Check for output redirection
    if "1>" in args:
        args = args.split(" 1> ")
        output_file = args[1]
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output = args[0].strip("'")
        with open(output_file, 'w') as f:
            f.write(output.strip())
    elif ">" in args:
        args = args.split(" > ")
        output_file = args[1]
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output = args[0].strip("'")
        with open(output_file, 'w') as f:
            f.write(output.strip())
    else:
        print(args)

def handler_exit(args=None):
    sys.exit(0)

def handler_pwd(args=None):
    print(os.getcwd())

def handler_cd(args=None):
    if args is None:
        return
    try:
        os.chdir(args)
    except FileNotFoundError:
        print("Directory not found")

def handler_cat(args=None):
    if args is None:
        return
    try:
        with open(args, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("File not found")

def handler_type(args=None):
    if args is None:
        return
    try:
        with open(args, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("File not found")

def main():
    while True:
        user_input = input("$ ")
        args = user_input.split()

        if args[0] == "echo":
            handler_echo(" ".join(args[1:]))
        elif args[0] == "exit":
            handler_exit()
        elif args[0] == "pwd":
            handler_pwd()
        elif args[0] == "cd":
            handler_cd(args[1])
        elif args[0] == "cat":
            handler_cat(args[1])
        elif args[0] == "type":
            handler_type(args[1])
        else:
            subprocess.run(args)

if __name__ == "__main__":
    main()