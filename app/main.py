import shutil
import sys

def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        builtin = ["exit", "echo", "type"]
        # Wait for user input
        command = input()
        if command == "exit" or command == "exit 0":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command.startswith("type"):
            if command[5:] in builtin:
                print(f"{command[5:]} is a shell builtin")
            else:
                path = shutil.which(command[5:])
                if path:
                    print(f"{command[5:]} is {path}")
                else:
                    print(f"{command[5:]}: not found")
        elif not command.strip():
            print("Please provide a command to check")
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()