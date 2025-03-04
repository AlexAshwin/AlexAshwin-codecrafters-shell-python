import sys
def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()
        command, *args = command.split(" ")
        if command == "exit 0":
            break
        elif command[0:4] == "echo":
            print(" ".join(args))
            main()
        else:
            print(f"{command}: command not found")
            main()
if __name__ == "__main__":
    main()
