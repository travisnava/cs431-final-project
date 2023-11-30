import mysql.connector
import os
import getpass
from datetime import date
from datetime import datetime


mydb = mysql.connector.connect(host="localhost", user="root", passwd="clashroyale5%")

# global var for currently logged in User, changed upon login
currentUser = None
adminLoggedIn = None

# ANSI escape code for green & red text
green_code = "\033[92m"
red_code = "\033[91m"

# Reset ANSI escape code to return to default text color
reset_code = "\033[0m"


def initDB():
    mycursor = mydb.cursor()
    mycursor.execute("USE sampleDB")


def exit():
    n = int(input(" Press 5 to exit : "))

    if n == 5:
        os.system("cls")  # For Windows
        run()
    else:
        print(" Invalid Option")
        exit()


def printLine():
    print("--------------------")


def userLogin():
    global currentUser
    global adminLoggedIn

    while currentUser == None:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        # query db for row that matches username
        mycursor = mydb.cursor()
        query = "SELECT * FROM Customers WHERE username = %s"
        mycursor.execute(query, (username,))
        user = mycursor.fetchall()

        if user:
            # correct login
            if password == user[0][1]:
                currentUser = user
                adminLoggedIn = False
                print(
                    green_code
                    + "Login success! Welcome, "
                    + user[0][0]
                    + "."
                    + reset_code
                )
            else:
                print(red_code + "Incorrect password, try again." + reset_code)
                printLine()
        else:
            print(red_code + "Incorrect login, try again." + reset_code)
            printLine()


# identical code to userLogin, just queries the Administrators table instead of Customers, could combine into one function?
def adminLogin():
    global currentUser
    global adminLoggedIn

    while currentUser == None:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        # query db for row that matches username
        mycursor = mydb.cursor()
        query = "SELECT * FROM Administrators WHERE username = %s"
        mycursor.execute(query, (username,))
        user = mycursor.fetchall()

        if user:
            # correct login
            if password == user[0][1]:
                currentUser = user
                adminLoggedIn = True
                print(
                    green_code
                    + "Login success! Welcome, "
                    + user[0][0]
                    + "."
                    + reset_code
                )
            else:
                print(red_code + "Incorrect password, try again." + reset_code)
                printLine()
        else:
            print(red_code + "Incorrect login, try again." + reset_code)
            printLine()


def displayUserMainMenu():
    print("------- MENU -------")
    print("  1. View all movie theaters")
    print("  2. Search for a movie theater")
    print("  3. View all movies playing at a movie theater")
    print(
        "  4. View a list of all movies now playing at a movie theater sorted by release date"
    )
    print(
        "  5. View a list of movies with the highest average ratings, along with the theaters where they are currently playing"
    )
    print(
        "  6. Buy a ticket for a movie screening"
    )  # Transaction that uses rollback, not sure how to implement... query #12 from Stage 3, replaces query #4 from Stage 3
    print("  7. Cancel a booking for a movie screening")
    print("  8. Search for concessions at a movie theater")
    print("  9. View a list of all movie ratings given by a specific customer")
    print(
        "  10. Leave a rating for a movie that you've seen"
    )  # The SQL needs to be edited for this...
    print("  11. Exit")
    printLine()


# Should admins have all the same menu options as users?
def displayAdminMainMenu():
    print("------- MENU -------")
    print("  1. View all movie theaters")
    print("  2. Search for a movie theater")
    print("  3. Delete movie theater by ID")
    print("  4. View all movies playing at a movie theater")
    print("  5. Add a new movie")
    print("  6. Update a movie's information")
    print("  7. Delete movie by ID")
    print("  8. Create a new screening for a movie at a theater")
    print("  9. Delete movie screening by ID")
    print("  10. Search for concessions at a movie theater")
    print("  11. Exit")
    printLine()


def getAllMovieTheaters():
    mycursor = mydb.cursor()
    print("------ All Theaters ------\n")
    mycursor.execute("SELECT * FROM MovieTheaters")
    theaterList = mycursor.fetchall()

    for theater in theaterList:
        print(" -----", theater[1], "-----")
        print(" Location : ", theater[2])
        print(" Capacity : ", theater[3])
        print("\n")

    print("------ SUCCESS ------\n")
    exit()


# needs error handling for nonexistent ID selected
def deleteTheaterByID():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM MovieTheaters")
    theaterList = mycursor.fetchall()
    print("Theater ID | Theater Name")
    for theater in theaterList:
        printLine()
        print(str(theater[0]) + "|" + theater[1])
    printLine()
    deleteThisTheater = int(
        input("\nEnter the theater id of the movie theater you wish to delete: ")
    )
    query = "DELETE FROM MovieTheaters WHERE theater_id = %s"
    mycursor.execute(query, (deleteThisTheater,))
    os.system("cls")
    mydb.commit()
    mycursor.execute("SELECT * FROM MovieTheaters")
    theaterList = mycursor.fetchall()
    print("Theater ID | Theater Name")
    for theater in theaterList:
        printLine()
        print(str(theater[0]) + "|" + theater[1])
    mycursor.close()


# needs error handling for release date format and movie_name & description are correct type?
def addNewMovie():
    movie_name = input("Enter the movie name: ")
    movie_description = input("Enter the movie's description: ")
    release_date = input("Enter a release date in the format of YYYY-MM-DD: ")
    query = "INSERT INTO Movies (movie_name, movie_description, release_date) VALUES (%s, %s, %s)"
    values = (movie_name, movie_description, release_date)
    mycursor = mydb.cursor()
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()


def updateMovieByID():
    mycursor = mydb.cursor()
    # Displaying current movies table
    mycursor.execute("SELECT * FROM Movies")
    moviesList = mycursor.fetchall()
    print("Movie ID | Movie Title | Movie Description | Release Date")
    for movie in moviesList:
        printLine()
        print(
            str(movie[0])
            + "|"
            + movie[1]
            + "|"
            + movie[2]
            + "|"
            + movie[3].strftime("%Y-%m-%d")
        )
    printLine()

    # Prompting user for updated movie information
    # Wrap in a try catch block to prevent incorrect release date format? Can catch value error...
    movie_id_to_update = input(
        "\nEnter the movie id for the movie you wish to update: "
    )
    updated_title = input("Enter the updated movie title: ")
    updated_description = input("Enter the updated movie description: ")
    updated_release_date = input(
        "Enter the updated movie release date in YYYY-MM-DD format: "
    )
    query = "UPDATE Movies SET movie_name = %s, movie_description = %s, release_date = %s WHERE movie_id = %s"
    values = (
        updated_title,
        updated_description,
        datetime.strptime(updated_release_date, "%Y-%m-%d"),
        movie_id_to_update,
    )
    mycursor.execute(query, values)
    mydb.commit()

    # Displaying updated movies table
    os.system("cls")
    mycursor.execute("SELECT * FROM Movies")
    updatedMoviesList = mycursor.fetchall()
    print("Movie ID | Movie Title | Movie Description | Release Date")
    for updatedMovie in updatedMoviesList:
        printLine()
        print(
            str(updatedMovie[0])
            + "|"
            + updatedMovie[1]
            + "|"
            + updatedMovie[2]
            + "|"
            + updatedMovie[3].strftime("%Y-%m-%d")
        )
    printLine()
    mycursor.close()


def displayMainMenu():
    print("------- MENU -------")
    print("  1. User login")
    print("  2. Admin login")
    print("  3. Exit")
    printLine()


def run():
    displayMainMenu()
    n = int(input("Enter option : "))
    if n == 1:
        os.system("cls")  # For Windows
        userLogin()
    elif n == 2:
        os.system("cls")
        adminLogin()
    elif n == 3:
        os.system("cls")
        print(" — — — Thank You — — -")
        return
    else:
        # os.system("cls")
        run()

    if not adminLoggedIn:
        # User is logged in
        displayUserMainMenu()
        n = int(input("Enter option : "))
        if n == 1:
            os.system("cls")  # For Windows
            getAllMovieTheaters()
        elif n == 2:
            os.system("cls")
            # insert function here
        elif n == 3:
            os.system("cls")
            deleteTheaterByID()
        elif n == 4:
            os.system("cls")
            # insert function here
        elif n == 5:
            os.system("cls")
            # insert function here
        elif n == 6:
            os.system("cls")
            # insert function here
        elif n == 7:
            os.system("cls")
            # insert function here
        elif n == 8:
            os.system("cls")
            # insert function here
        elif n == 9:
            os.system("cls")
            # insert function here
        elif n == 10:
            os.system("cls")
            # insert function here
        elif n == 11:
            os.system("cls")
            print(" — — — Thank You — — -")
        else:
            # os.system("cls")
            run()

    else:
        # Admin is logged in
        displayAdminMainMenu()
        n = int(input("Enter option : "))
        if n == 1:
            os.system("cls")  # For Windows
            getAllMovieTheaters()
        elif n == 2:
            os.system("cls")
            # insert function here
        elif n == 3:
            os.system("cls")
            deleteTheaterByID()
        elif n == 4:
            os.system("cls")
            # insert function here
        elif n == 5:
            os.system("cls")
            addNewMovie()
        elif n == 6:
            os.system("cls")
            updateMovieByID()
        elif n == 7:
            os.system("cls")
            # insert function here
        elif n == 8:
            os.system("cls")
            # insert function here
        elif n == 9:
            os.system("cls")
            # insert function here
        elif n == 10:
            os.system("cls")
            # insert function here
        elif n == 11:
            os.system("cls")
            print(" — — — Thank You — — -")
        else:
            # os.system("cls")
            run()


def displayLogo():
    print(
        """
          


.___  ___.   ______   ____    ____  __   _______    .___  ___.      ___      .__   __.      ___       _______  _______ .______      
|   \/   |  /  __  \  \   \  /   / |  | |   ____|   |   \/   |     /   \     |  \ |  |     /   \     /  _____||   ____||   _  \     
|  \  /  | |  |  |  |  \   \/   /  |  | |  |__      |  \  /  |    /  ^  \    |   \|  |    /  ^  \   |  |  __  |  |__   |  |_)  |    
|  |\/|  | |  |  |  |   \      /   |  | |   __|     |  |\/|  |   /  /_\  \   |  . `  |   /  /_\  \  |  | |_ | |   __|  |      /     
|  |  |  | |  `--'  |    \    /    |  | |  |____    |  |  |  |  /  _____  \  |  |\   |  /  _____  \ |  |__| | |  |____ |  |\  \----.
|__|  |__|  \______/      \__/     |__| |_______|   |__|  |__| /__/     \__\ |__| \__| /__/     \__\ \______| |_______|| _| `._____|



"""
    )


if __name__ == "__main__":
    initDB()
    displayLogo()
    run()
