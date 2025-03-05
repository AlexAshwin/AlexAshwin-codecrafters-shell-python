import sys
from os import chdir, environ, getcwd, path, listdir
import shlex
from contextlib import redirect_stdout, redirect_stderr
from subprocess import run, PIPE
import readline

# List of built-in commands
all_builtin_cmd = ["exit", "echo", "type", "pwd", "cd"]

# Completer function that includes executables
def completer(text, state):
    # First try to complete built-in commands
    completions = [cmd for cmd in all_builtin_cmd if cmd.startswith(text)]
    
    # Also try to complete executables from the system PATH
    if not completions:
        PATH_ENV = environ["PATH"].split(":")
        for path_dir in PATH_ENV:
            try:
                # Check if there are files that match the input text
                files = [f for f in listdir(path_dir) if f.startswith(text) and path.isfile(path.join(path_dir, f))]
                completions.extend(files)
            except FileNotFoundError:
                continue
    
    # Return the nth completion
    if state < len(completions):
        return completions[state] + " "
    return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def main():
    sys.stdout.write("$ ")
    cmd = input()
    
    # Handle built-in commands directly
    if cmd in all_builtin_cmd:
        handle_cmd(cmd)
    else:
        # Handle commands with redirection
        match shlex.split(cmd):
            case [*run_cmd, ">>", file] | [*run_cmd, "1>>", file]:
                with open(file, "a") as out_file:
                    with redirect_stdout(out_file):
                        handle_cmd(" ".join(run_cmd))
            case [*run_cmd, ">", file] | [*run_cmd, "1>", file]:
                with open(file, "w") as out_file:
                    with redirect_stdout(out_file):
                        handle_cmd(" ".join(run_cmd))
            case [*run_cmd, "2>>", file]:
                with open(file, "a") as err_file:
                    with redirect_stderr(err_file):
                        handle_cmd(" ".join(run_cmd))
            case [*run_cmd, "2>", file]:
                with open(file, "w") as err_file:
                    with redirect_stderr(err_file):
                        handle_cmd(" ".join(run_cmd))
            case _:
                handle_cmd(cmd)

    main()

def handle_cmd(cmd):
    match shlex.split(cmd):
        case ["exit", "0"]:
            sys.exit(0)
        case ["echo", *args]:
            print(*args)
        case ["type", arg]:
            print(type_cmd(arg)[1])
        case ["pwd"]:
            print(getcwd())
        case ["cd", arg]:
            cd_cmd(arg)
        case [found_cmd, *args] if type_cmd(found_cmd)[0]:
            process = run(shlex.split(cmd), stdout=PIPE, stderr=PIPE, text=True)
            print(process.stdout, end="")
            if process.stderr:
                print(process.stderr, file=sys.stderr, end="")
        case _:
            print(f"{cmd}: command not found", file=sys.stderr)

def type_cmd(cmd):
    if cmd in all_builtin_cmd:
        return False, f"{cmd} is a shell builtin"
    PATH_ENV = environ["PATH"].split(":")
    for path_dir in PATH_ENV:
        file_path = path.join(path_dir, cmd)
        if path.isfile(file_path):
            return True, f"{cmd} is {file_path}"
    return False, f"{cmd}: not found"

def cd_cmd(arg):
    try:
        chdir(path.expanduser(arg))
    except OSError:
        print(f"cd: {arg}: No such file or directory", file=sys.stderr)

if __name__ == "__main__":
    main()
