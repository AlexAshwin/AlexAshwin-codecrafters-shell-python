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
            if  path := shutil.which(command[5:]):
                 print(f"{command[5:]} is {path}")
            elif command[5:] in builtin:
                print(f"{command[5:]} is a shell builtin")
            else:
                print(f"{command[5:]}: not found")
        elif command[5:] == "":
            print("Please provide a command to check")
if __name__ == "__main__":
    main()
