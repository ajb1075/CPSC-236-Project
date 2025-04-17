import pandas as pd
import random
from IPython.display import clear_output

def checkUser():
    firstName = ""
    lastName = ""
    userID = ""
    x = 3
    
    firstName = input("Please enter your first name: ")
    lastName = input("Please enter your last name: ")
    userID = input("Please enter your ID: ")
    
    while x > 0:
        if len(userID) != 6 or userID == "":
            print("Incorrect length.")
        elif userID[0] != "A":
            print("Invalid start.")
        elif userID[1:].isdigit == False:
            print("Only digits allowed.")
        else:
            print("Welcome", firstName + "!")
            break
            
        x-=1
        if x > 0:
            userID = input("\nPlease enter a valid ID. You have " + str(x) + " chances remaining.")
        else:
            print("No chances remaining.")

    return firstName, lastName, userID

def getChoices(end):
    randomChoices = []
    for i in range(0, end):
        tempRandom = random.randint(0, 128)
        randomChoices.append(tempRandom)
    return(randomChoices)

def main():
    while True:
        try:
            dataframe = pd.read_excel("CPSC 236 TestBank.xlsx")
        except FileNotFoundError:
            print("Test bank not found.")
            break
        correct = 0
        numQuestions = 10
        writeQuestions = {"Number":{}}
        
        firstName, lastName, userID = checkUser()
        choices = getChoices(numQuestions)
    
        for i in range(0, numQuestions):
            try:
                row = dataframe.iloc[choices[i]]
            except IndexError:
                print("Error at index", i)
            
            print("\nQuestion:", row.iloc[0], "\nOption A:", row.iloc[1], "\nOption B:", row.iloc[2])
            if not pd.isnull(row.iloc[3]):
                print("Option C:", row.iloc[3])
    
            userAns = input("\nYour answer:").upper()
    
            tempDict = {"Question": row.iloc[0], "Correct": row.iloc[4], "Answered": userAns}
            writeQuestions[i] = tempDict
            
            if userAns == row.iloc[4]:
                correct+=1
    
        print("\nOut of", numQuestions, "you got", correct, "correct.")
    
        fileName = userID + "_" + firstName + "_" + lastName + ".txt"
        with open(fileName, "w") as studentFile:
            studentFile.write(userID + ": " + firstName + " " + lastName)
            studentFile.write("\nScore: " + str(correct))
            studentFile.write("\nTime elapsed: ")
            for i in range(0,len(writeQuestions)-1):
                studentFile.write("\n" + writeQuestions[i]["Question"] + "\nCorrect answer: " + writeQuestions[i]["Correct"] + "\nGiven answer: " + writeQuestions[i]["Answered"])
    
        while True:
            endOption = input("A file with your results has been created. Enter Q to quit or S to clear the screen for the next student: ").upper()

            if endOption in ('Q', 'S'):
                break
            else:
                print("Please enter a valid option.")
            
        if endOption == "Q":
            print("Goodbye.")
            break
        elif endOption == "S":
            clear_output()
            continue

if __name__ == "__main__":
    main()
