# filenames = " file1.txt, file2.txt , file3.txt "
# y = filenames.split(",")
# print(y)
# Output: [' file1.txt', ' file2.txt ', ' file3.txt ']

# Split a string into a list where each word is a list item:

# txt = "welcome to the jungle"

# x = txt.split()

# print(x)

# # Split the string, using comma, followed by a space, as a separator:

# txt = "hello, my name is Peter, I am 26 years old"

# x = txt.split(", ")

# print(x)

# removes specified character
# txt = ",,,,,rrttgg.....banana....rrr"

# x = txt.strip(",.grt")

# print(x)

#   STRIP - REMOVES WS
#   SPLIT - SEPERATES ITEMS INTO A LIST(DEFAULT USES WHITESPACE unless specified)
#   LOWER - CONVERTS TO LOWERCASE
#   UPPER - CONVERTS TO UPPERCASE
#   TITLE - CONVERTS TO TITLECASE

#   JOIN - TAKES A LIST AND COMBINES IT INTO A STRING 
#   string.join(iterable)

# Join all items in a tuple into a string, using a hash character as separator:

myTuple = ("John", "Peter", "Vicky")

x = "#".join(myTuple)


myDict = {"name": "John", "country": "Norway"}
mySeparator = "TEST"

x = mySeparator.join(myDict)

print(x)



# filenames = input("Enter filenames to send (separated by commas): ").strip()
# filenames_list = [filename.strip() for filename in filenames.split(",")]

# print(filenames_list)

# fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
# newlist = []

# for fruit in fruits:
#     if "a" in fruit:
#         newlist.append(fruit)

# print(newlist)

# With list comprehension you can do all that with only one line of code:

# Example
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

# newlist = [fruit for fruit in fruits if "a" in fruit]


# Expression
# The expression is the current item in the iteration, but it is also the outcome, which you can manipulate before it ends up like a list item in the new list:

# Example
# Set the values in the new list to upper case:

newlist = [fruit.upper() for fruit in fruits]
print(newlist)


# The Syntax
# newlist = [expression for item in iterable if condition == True]

# from tqdm import tqdm
# for i in tqdm(range(10000)):
#     pass

