--[[
Name: Jackson Knapp
Date: 2/20/26
Purpose: A guessing game that allows the user to enter 7 guesses at a randomly generated number.
         A winning/losing condition is printed. The user can restart the game at the end
]]

randomInt = 0
attempts = 1
userInput = -1
math.randomseed(os.time())
math.random(); math.random()

-- Welcome banner and game instructions
print(" === Welcome to The Guessing Game === ")
print("\nYou have seven attempts to enter a correct guess between 1 and 100.\n")

while userInput ~= 0 do

    randomInt = math.random(1,100)

    -- While loop exits if maximum attempts are reached, or the user enters the correct number
    while attempts <= 7 and randomInt ~= userInput do
        print("Input guess #" .. attempts .. ": ")


        -- Validates input
        localInput = tonumber(io.read())
        isInteger = math.tointeger(localInput)
        if isInteger == nil then
            print("\nInvalid input entered.\n")
        else
            userInput = localInput
        end

        -- Player hints
        if attempts < 7 and userInput ~= randomInt and isInteger ~= nil then
            if userInput > randomInt then
                print("Target number is lower, try again\n")
            else
                print("Target number is higher, try again\n")
            end
        end

        -- Increments attempts
        attempts = attempts + 1

    end

    -- Prints winning / losing conditions
    if randomInt == userInput then
        print("\nWinning number found!: " .. randomInt)
    else
        print("\nNo correct number found...")
    end

    -- Reset variables
    attempts = 1
    randomInt = 0

    -- Player decides whether to restart
    print("\nPress 0 to exit game, press anything else to restart.")
    userInput = tonumber(io.read())

    -- Prints a restart message if the user selected 0, otherwise the game ends.
    if userInput ~= 0 then
        print("\nGame Restarting!\n")
        print("\nYou have seven attempts to enter a correct guess between 1 and 100.\n")
    end

end

print ("\nGame ended...")