import sys
def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()
        command, *args = command.split(" ")
        if command == "exit":
            break
        elif command[0:4] == "echo":
            print(" ".join(args))
        else:
            print(f"{command}: command not found")
if __name__ == "__main__":
    main()
