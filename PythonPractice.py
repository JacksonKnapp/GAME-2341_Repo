import random

# print("Hello")

# myvariable = 5

# def myfunction(x , y):
#         return (x + y)

# print(myfunction(myvariable, 10))

# mylist = [1, 2, 3, 4, 5, 78, 92, "bob"]

# for x in mylist:
#         print(x)

# mydictionary = {"name" : "george", "age" : 42}

# #this is a comment
# #print out the values of a dictionary
# for x in mydictionary:
#     print(mydictionary[x])

# for x in range (5):
#     print("hello")

# age = input("What is your age?")

# while not age.isdigit():
#     print("That is not a number :(")
#     age = input("What is your age?")

# print(age)

#Task #1
#Convert tex to uppercase, print the result

text = "text"
print(text.upper())

# #Task #2
# #Ask the user for 2 numbers, add them together, print the result

for i in range(2):
    total = 0
    num = input("Enter a number")

    while not num.isdigit():
        print("Incorrect, please enter a number.")
        num = input("Enter a number")

    total = int(num) + total

print("Final value: ", total)

#Task #3
#Get an unknown amount of numbers from the user, add them together, print the result
#Loop asking the user for numbers until they say there are done

total = 0
num = 0
while not (int(num) == -1):
    num = input("Enter a number: ")

    while not num.isdigit():
        print("Incorrect, please enter a number.")
        num = input("Enter a number: ")

    total = int(num) + total
    print("\nTotal: ", total, "\n")

    num = input("Enter -1 to finish: ")

    while not num.isdigit():
        print("Incorrect, please enter a number.")
        num = input("Enter a number: ")

print("\nFinal Total: ", total, "\n")

#Task #4
#Ask the user for a maximum number, generate a random number between 0 and their number, print the result
#Ask the user to play again

while True:
    num = input("Enter a number: ")

    while not num.isdigit() and num > 0:
        print("Incorrect, please enter another number.")
        num = input("Enter a number: ")

    print(random.randint(0, int(num)))
    if input("\nPress y to play again: ") != "y":
        break

print("Exited")
    
#Task #5
#Generate 10 random numbers, if they are even print "right" and if they are odd print "left"
#Print how many right vs left


left = 0
right = 0
for x in range(10):
    if random.randint(0,100) % 2 == 0:
        print("Right")
        right += 1
    else:
        print("Left")
        left += 1

print("Total Left: ", left, "   Total Right: ", right)





