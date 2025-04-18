import pandas as pd
import random
import sys
import os
import time
#from IPython.display import clear_output

""" Gets valid details from user """
def checkUser():
    firstName = ""
    lastName = ""
    userID = ""
    x = 3
    
    while True:
        firstName = input("Please enter your first name: ")
        lastName = input("Please enter your last name: ")

        if firstName == "" or lastName == "":
            print("One or both names invalid. Please try again.\n")
        elif firstName.isalpha() == False or lastName.isalpha() == False:
            print("Only alphabetic characters allowed.\n")
        else:
            break

    userID = input("Please enter your ID: ")
    
    #give user 3 chances to enter valid ID
    while x > 0:
        if len(userID) != 6 or userID == "":
            print("Incorrect length.")
        elif userID[0] != "A":
            print("Invalid start.")
        elif userID[1:].isdigit() == False:
            print("Only digits allowed after \"A\".")
        else:
            firstName = firstName.capitalize()
            lastName = lastName.capitalize()
            print("\nWelcome", firstName + "!")
            break
            
        x-=1
        if x > 0:
            userID = input("\nYou have " + str(x) + " chances remaining. Please enter a valid ID: ")
        else:
            print("\nNo chances remaining. Goodbye.")
            sys.exit()

    return firstName, lastName, userID

""" Gets number of questions for quiz, 10 or 20 """
def askNumQuestion():
    while True:
        ans = input("\nWould you prefer 10 or 20 questions? ")
        if ans not in ('10', '20'):
            print("Please enter either \"10\" or \"20\".")
        elif ans == "20":
            return int(ans), .5
        else:
            return int(ans), 1

""" Randomly chooses questions without duplicates """
def getChoices(end):
    randomChoices = []
    for i in range(0, end):
        randomChoices = random.sample(range(0, 128), end)
    return(randomChoices)

""" Prints questions and gets user input for question answers"""
def getAns(row, correct):
    options = ['A', 'B'] #keep track of options available in current question

    #print questions, only including option c if not null
    print("\nQuestion:", row.iloc[0], "\nOption A:", row.iloc[1], "\nOption B:", row.iloc[2])
    if not pd.isnull(row.iloc[3]):
        print("Option C:", row.iloc[3])
        options.append('C')

    #validate user input
    while True:
        userAns = input("\nYour answer: ").upper()
        if userAns in options:
            break
        else:
            print("Please enter a valid option.")

    #info to add to file at end
    tempDict = {"Question": row.iloc[0], "Correct": row.iloc[4], "Answered": userAns}
    
    if userAns == row.iloc[4]:
        correct+=1

    return tempDict, correct

""" Uses start time & end time to create elapsed time for user file at end """
def convertTime(startTime, endTime):
    elapsed = endTime - startTime
    minutes = int(round(elapsed // 60, 0))
    seconds = int(round((elapsed % 60), 0))
    print(f"Finished in {endTime - startTime:.1f} seconds")
    elapsed = str(minutes) + " minutes " + str(seconds) + " seconds"

    return elapsed

def main():
    while True: #loop if quit option not chosen at end
        #read excel file into pandas dataframe
        try:
            dataframe = pd.read_excel("CPSC 236 TestBank.xlsx")
        except FileNotFoundError:
            print("Test bank not found.")
            break
        except Exception as e:
            print("Error with file:", type(e), e)
            break

        correct = 0
        firstName, lastName, userID = checkUser()
        numQuestions, weight = askNumQuestion()
        choices = getChoices(numQuestions)
        writeQuestions = {"Number":{}}
    
        startTime = time.perf_counter()
        timeout = time.time() + 30 * 3

        #grab questions and answers associated with randomly chosen indices
        for i in range(0, numQuestions):
            try:
                row = dataframe.iloc[choices[i]]
            except IndexError:
                print("Error at index", i)
            except Exception as e:
                print("Error fetching question:", type(e), e)
            
            #have user answer each question and store input
            if time.time() < timeout:
                tempDict, correct = getAns(row, correct)
                writeQuestions[i] = tempDict
            else:
                break

        #determine end time of quiz and prep elapsed time for user file
        endTime = time.perf_counter()
        elapsed = convertTime(startTime, endTime)

        #give user score out of 10
        print("\nOut of", numQuestions, "you got", correct, "correct.")
        score = correct * weight
        print("Your score is:", str(score) + "/10.")
    
        #write results to user file
        fileName = userID + "_" + firstName + "_" + lastName + ".txt"
        with open(fileName, "w") as studentFile:
            studentFile.write(userID + ": " + firstName + " " + lastName)
            studentFile.write("\nScore: " + str(correct) + "\nTime elapsed: " + elapsed + "\n\nQuestions:\n")
            for i in range(0,len(writeQuestions)-1):
                studentFile.write(writeQuestions[i]["Question"] + "\nCorrect answer: " + writeQuestions[i]["Correct"] + "\nGiven answer: " + writeQuestions[i]["Answered"] + "\n\n")
    
        #make sure user picks one of the end options
        while True:
            endOption = input("\nA file with your results has been created. Enter Q to quit or S to clear the screen for the next student: ").upper()

            if endOption in ('Q', 'S'):
                break
            else:
                print("Please enter a valid option.")
            
        #exit if quit chosen, otherwise loop back to start
        if endOption == "Q":
            print("\nGoodbye.")
            break
        elif endOption == "S":
            #clear_output()
            os.system('cls')
            continue

if __name__ == "__main__":
    main()