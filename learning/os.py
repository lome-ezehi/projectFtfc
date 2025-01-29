import os

# print(dir(os))
# print(os.getcwd()) #Show current directory

os.chdir("/Users/newuser/Desktop/")
# print(os.getcwd()) #Show current directory
# making directories
# os.mkdir('OS-Demo-2')
# os.makedirs('OS-Demo-2/sub-directory')
# Delete
# os.rmdir()
# os.removedirs('OS-Demo-2/sub-directory'
# rename
# os.rename('text.txt', 'test.txt')
# check file info
# print(os.stat("test.txt").st_size) #sixe
# environ variables
# print(os.environ.get("HOME"))


# os.path() #j0ins direcories(/)
# file_path = os.path.join(os.environ.get("HOME"), 'os-lome.txt')
# print(file_path)
# os.path.dirname("/Users/newuser/Desktop/") #Prints directory name
# os.path.basename("/Users/newuser/Desktop/")
print(os.path.split("/Users/newuser/")) # prints the 2
print(os.path.isdir("/Users/newuser/Desktop/")) # Checks if path is directory
print(os.path.isfile("/Users/newuser/Desktop/")) # Checks if path is file
print(os.path.exists("/Users/newuser/Desktop/")) # Checks if path exists
# CHECK ALL WITH
# print(dir(os.path))

# print(os.listdir()) #Show current directory