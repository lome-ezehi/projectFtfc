#!/usr/bin/python3

import cmd
import os
import subprocess


class RunScripts(cmd.Cmd):
    """ A command line based tool for running Python scripts """

    prompt = 'run ... '

    def preloop(self):
        intro = (
            "Welcome to socket programming, I created this tool for running Python scripts\n"
            "Type 'help' for a list of available commands.\n"
            "Type '<help> <command>' to see specific command help."
        )
        print(intro)

    def do_run(self, arg):
        """Runs a Python script.

        Usage: run <script_name.py>
        """
        if not arg:
            print("Please provide a script name.")
            return

        script_path = arg.strip()  # Remove leading/trailing whitespace

        if not script_path.endswith(".py"):
            script_path += ".py"  # Automatically add .py extension if not provided

        if not os.path.exists(script_path):
            print(f"Script '{script_path}' not found.")
            return

        try:
            # Use subprocess.run for better control and error handling
            result = subprocess.run(
                ['python3', script_path], capture_output=True, text=True, check=True
            )
            print(result.stdout)  # Print the script's output
        except subprocess.CalledProcessError as e:
            print(f"Error running script '{script_path}':")
            print(e.stderr)  # Print the script's error messages
        except FileNotFoundError:
            print("Python interpreter not found. Make sure Python is in your PATH.")
        except Exception as e:  # Catch other potential errors (e.g., script syntax errors)
            print(f"An unexpected error occurred: {e}")

    def do_quit(self, arg):
        """ Quits the command interpreter """
        return True

    def do_greet(self, arg):
        """ Greets people """
        if len(arg) == 0:
            print("Provide an argument")
        else:
            name = arg.strip()
            print(f"Hello {name}")

    def emptyline(self):
        """ Method called when an empty line is entered """
        return

    def do_EOF(self, arg):
        """ Exits command interpreter when it receives (Ctrl + D or Command + D) """
        print()
        return True

    def postloop(self):
        print('Exiting... Goodbye!')


if __name__ == "__main__":
    RunScripts().cmdloop()