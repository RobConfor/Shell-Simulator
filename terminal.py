import curses
import sys 
import argparse


def parse_command(command):
    parser = argparse.ArgumentParser(exit_on_error=False)

    subparsers = parser.add_subparsers(dest='command')

    math_parser = subparsers.add_parser('math')
    math_parser.add_argument('num1', type=int, help='First number')
    math_parser.add_argument('operator', choices=['+', '-', '*', '/'], help='Operator')
    math_parser.add_argument('num2', type=int, help='Second number')

    help_parser = subparsers.add_parser('help')

    try:
        args = parser.parse_args(command.split())
        return args
    except:
        return None


def main(stdscr):
    stdscr.scrollok(True)
    stdscr.clear()
    stdscr.refresh()
    command_history = []
    history_index = 0

    while True:
        stdscr.addstr("> ")
        stdscr.refresh()
        command = ""
        curr_pos = len(command_history)
        temp_command = ""
        x = curses.getsyx()[1]

        # key pressing / waiting for enter to be pushed
        # handles command history and cursor nav
        while True:
            key = stdscr.getkey()
            if key == '\n':
                stdscr.move(curses.getsyx()[0], 2)
                stdscr.clrtoeol()
                stdscr.addstr(command)
                stdscr.refresh()
                break
            elif key == 'KEY_UP':
                if curr_pos > 0:
                    if curr_pos == len(command_history):
                        temp_command = command
                    curr_pos -= 1
                    stdscr.move(curses.getsyx()[0], 2)
                    stdscr.clrtoeol()
                    command = command_history[curr_pos]
                    stdscr.addstr(command)
                    x = len(command) + 2
            elif key == 'KEY_DOWN':
                if curr_pos < len(command_history):
                    curr_pos += 1
                    stdscr.move(curses.getsyx()[0], 2)
                    stdscr.clrtoeol()
                    if curr_pos == len(command_history):
                        command = temp_command
                    else:
                        command = command_history[curr_pos]
                    stdscr.addstr(command)
                    x = len(command) + 2
            elif key == '\x7f' or key == '\b': 
                if len(command) > 0 and x > 2:
                    delete_pos = x - 3  
                    command = command[:delete_pos] + command[delete_pos + 1:]
                    stdscr.move(curses.getsyx()[0], 2)
                    stdscr.clrtoeol()
                    stdscr.addstr(command)
                    x -= 1
                    stdscr.move(curses.getsyx()[0], x)
                    stdscr.refresh()
            elif key == 'KEY_LEFT':
                if x > 2: 
                    x -= 1
                    stdscr.move(curses.getsyx()[0], x)
                    stdscr.refresh()
            elif key == 'KEY_RIGHT':
                if x < len(command) + 2:
                    x += 1
                    stdscr.move(curses.getsyx()[0], x)
                    stdscr.refresh()
            elif key == 'KEY_RESIZE':
                    stdscr.refresh()
                    continue

            elif key.isprintable():
                insert_pos = x - 2  
                command = command[:insert_pos] + key + command[insert_pos:]
        
                stdscr.move(curses.getsyx()[0], 2)
                stdscr.clrtoeol()  
                stdscr.addstr(command)  
                x += 1  
                stdscr.move(curses.getsyx()[0], x)  
                stdscr.refresh()

            else:
                command += key
                stdscr.addstr(key)
                stdscr.refresh()
                
                
        # command parsing 
        if command == "exit":
            break
        else: 
            stdscr.addstr("\n")
            if command != "":
                command_history.append(command)
            stdscr.refresh()

            if "math" in command:
                args = parse_command(command)

                if args is None:
                    stdscr.addstr("\nInvalid command. Type 'help' for usage.\n")
                    continue
                elif args.command == "math":
                    try:
                        result = None
                        if args.operator == '+':
                            result = args.num1 + args.num2
                        elif args.operator == '-':
                            result = args.num1 - args.num2
                        elif args.operator == '*':
                            result = args.num1 * args.num2
                        elif args.operator == '/':
                            result = args.num1 / args.num2
                        
                        stdscr.addstr(f"\nResult: {result}\n")
                    except Exception as e:
                        stdscr.addstr(f"\nError: {str(e)}\n")
                    
                elif args.command == "help":
                    continue
            elif command == "help":
                stdscr.addstr("\nCommands: math \n")
                stdscr.addstr("\nUsage: <int> <operator> <int> \n\tPreforms an operation on two numbers \n")
                stdscr.refresh()
            
if __name__ == '__main__':
    curses.wrapper(main)
