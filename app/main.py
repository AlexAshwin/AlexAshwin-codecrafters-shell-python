import sys
def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()
        builtin = ['type','echo','exit']
        if command == "exit" or command == "exit 0":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command.startswith("type"):
            if command[5:] in builtin:
                print(f"{command[5:]} is a shell builtin")
            elif command[5:] == "":
                print("Please provide a command to check") 
            else:
                print(f"{command[5:]}: not found")
        else:
            print(f"{command}: command not found")
if __name__ == "__main__":
    main()
