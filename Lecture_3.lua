--[[

--#1
--Ask the user for some text, convert the text into all caps

print("PLease enter some words")
userInput = io.read()
print(string.upper(userInput))

--#2
--Ask the user for 2 numbers, add them together, print the result

print("Please enter two numbers")
numOne = tonumber(io.read())

while numOne == nil do
    print("That is not a number, try again!")
    numOne = tonumber(io.read())
end

numTwo = tonumber(io.read())

while numTwo == nil do
    print("That is not a number, try again!")
    numTwo = tonumber(io.read())
end

total = numOne + numTwo
print("The sum is: " .. total)


--#3
--Get an unknown amount of numbers from the user, add them together, print out the result

controlVar = "y"
total = 0
inputNum = 0

while controlVar == "y" do
    print("Enter a number")
    inputNum = tonumber(io.read())

    while inputNum == nil do
        print("Not a number, try a gain")
        inputNum = tonumber(io.read())
    end

    total = total + inputNum
    print("Do you want to enter another number? y or n")
    controlVar = io.read()

end

print("The total is " .. total)



--#4
--Have the user define a maximum number, print out a random number between 0 and their number
--Have the user play again or quit


playAgain = "y"
math.randomseed(os.time())
math.random(); math.random(); math.random()

while playAgain == "y" do
    print("Enter a maximum number")
    userMaximum = tonumber(io.read())

    while userMaximum == nil do
        print("Not a number, try a gain")
        userMaximum = tonumber(io.read())
    end

    randomNum = math.random(0, userMaximum)
    print("Random number is: " .. randomNum)

    print("Enter y to restart")
    playAgain = io.read()

end

]]

--#5
--Get a random number, if the number is even print "EVEN" if it is odd print "ODD", do this 10 times. Print how many times it was odd
--and how many times it was even.
--We gotta use modulus! %

math.randomseed(os.time())
math.random(); math.random()
even = 0
odd = 0


for i = 0, 9 do
    rand = math.random(1,100)
    print(rand)
    if rand % 2 == 0 then
        print("Even")
        even = even + 1
    else
        print("Odd")
        odd = odd + 1
    end 
end

print("Even numbers: " .. even)
print("Odd numbers: " .. odd)