# Syntax Error (Error)
print("Hello world")  # Missing closing parenthesis

# ZeroDivisionError (Exception)


# try:
#     n=10
#     answer = n/0
# except ZeroDivisionError as e:
#     print(e)
# except ValueError as e: 
#     print(e)
# else:
#     print(answer)
# finally:
#     print("complete")


# with
try:
    f = open("os.py", "r")
    print(f.read())

    # f = open("os.py", "r")
    # for x in f:
    #     print(x)
except FileNotFoundError as e:
    print(e)
finally:
    f.close()



# "r" - Read - Default value. Opens a file for reading, error if the file does not exist

# "a" - Append - Opens a file for appending, creates the file if it does not exist

# "w" - Write - Opens a file for writing, creates the file if it does not exist

# "x" - Create - Creates the specified file, returns an error if the file exists

# In addition you can specify if the file should be handled as binary or text mode

# "t" - Text - Default value. Text mode

# "b" - Binary - Binary mode (e.g. images)

# Because "r" for read, and "t" for text are the default values, you do not need to specify them.


# WITH
with open('example.txt', 'r') as f:
    content = f.read()
    # Work with file content
# In this example:

# open('example.txt', 'r') returns a file object.
# as f assigns the file object to the variable f.
# Inside the with block, f is used to read the content of the file (f.read()).
# After exiting the with block, the file object f is automatically closed, releasing system resources.

