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
    printLine()
    n = int(input("\nPress 1 to main menu or 2 to exit: "))

    if n == 1:
        os.system("cls")  # For Windows
        run()
    elif n == 2:
        os.system("cls")
        print(" — — — Thank You — — -")
        return
    else:
        print("Invalid Option")
        exit()


def printLine():
    print("--------------------")


def userLogin():
    global currentUser
    global adminLoggedIn

    while currentUser == None or adminLoggedIn == True:
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

    while currentUser == None or adminLoggedIn == None or adminLoggedIn == False:
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
    print(
        "  3. View a list of all movies now playing at a movie theater sorted by release date descending"
    )
    print(
        "  4. View a list of movies with the highest average ratings, along with the theaters where they are currently playing"
    )
    print(
        "  5. Buy a ticket for a movie screening"
    )  # Transaction that uses rollback, not sure how to implement... query #12 from Stage 3, replaces query #4 from Stage 3
    print("  6. Cancel a booking for a movie screening")
    print("  7. Search for concessions at a movie theater")
    print("  8. View a list of all movie ratings given by a specific customer")
    print(
        "  9. Leave a rating for a movie that you've seen"
    )  # The SQL needs to be edited for this...
    print("  10. Exit")
    printLine()


# Should admins have all the same menu options as users?
def displayAdminMainMenu():
    print("------- MENU -------")
    print("  1. View all movie theaters")
    print("  2. Search for a movie theater")
    print("  3. Delete movie theater by ID")
    print(
        "  4. View a list of all movies now playing at a movie theater sorted by release date descending"
    )
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
    exit()


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

    mycursor.close()
    exit()


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
    exit()


# needs error handling for nonexistent ID selected
def deleteMovieByID():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Movies")
    movieList = mycursor.fetchall()
    print("Movie ID | Movie Name")
    for movie in movieList:
        printLine()
        print(str(movie[0]) + "|" + movie[1])
    printLine()
    deleteThisMovie = int(input("\nEnter the id of the movie you wish to delete: "))
    query = "DELETE FROM Movies WHERE movie_id = %s"
    mycursor.execute(query, (deleteThisMovie,))
    os.system("cls")
    mydb.commit()

    mycursor.execute("SELECT * FROM Movies")
    movieList = mycursor.fetchall()
    print("Movie ID | Movie Name")
    for movie in movieList:
        printLine()
        print(str(movie[0]) + "|" + movie[1])
    mycursor.close()
    exit()


# needs error handling for nonexistent ID selected
def deleteMovieScreeningByID():
    mycursor = mydb.cursor()
    selectQuery = """SELECT S.screening_id, M.movie_name, T.theater_name, S.screening_time
                FROM Screenings AS S
                INNER JOIN Movies AS M ON S.movie_id = M.movie_id 
                INNER JOIN MovieTheaters AS T ON S.theater_id = T.theater_id
                ORDER BY S.screening_time ASC
        """
    mycursor.execute(selectQuery)
    screeningList = mycursor.fetchall()
    print("Screening ID | Movie | Movie Theater | Screening Time")
    for screening in screeningList:
        printLine()
        print(
            str(screening[0])
            + "|"
            + str(screening[1])
            + "|"
            + str(screening[2])
            + "|"
            + screening[3].strftime("%Y-%m-%d %H:%M")
        )
    printLine()
    deleteThisScreening = int(
        input("\nEnter the id of the movie screening you wish to delete: ")
    )
    deleteQuery = "DELETE FROM Screenings WHERE screening_id = %s"
    mycursor.execute(deleteQuery, (deleteThisScreening,))
    os.system("cls")
    mydb.commit()

    mycursor.execute(selectQuery)
    screeningList = mycursor.fetchall()
    print("Screening ID | Movie | Movie Theater | Screening Time")
    for screening in screeningList:
        printLine()
        print(
            str(screening[0])
            + "|"
            + str(screening[1])
            + "|"
            + str(screening[2])
            + "|"
            + screening[3].strftime("%Y-%m-%d %H:%M")
        )
    mycursor.close()
    exit()


# needs error handling for release date format and movie_name & description are correct type?
def createNewMovieScreening():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM MovieTheaters")
    theaterList = mycursor.fetchall()
    print("Theater ID | Theater Name")
    for theater in theaterList:
        printLine()
        print(str(theater[0]) + "|" + theater[1])
    printLine()
    screeningForTheaterID = int(
        input(
            "\nEnter the theater id of the movie theater you wish to create a movie screening for: "
        )
    )
    os.system("cls")

    mycursor.execute("SELECT * FROM Movies")
    movieList = mycursor.fetchall()
    print("Movie ID | Movie Name")
    for movie in movieList:
        printLine()
        print(str(movie[0]) + "|" + movie[1])
    newScreeningMovieID = input(
        "\nSelect the movie id of the movie you wish to create a screening for: "
    )
    newScreeningTime = input("Enter a screening time in the YYYY-MM-DD HH:MM format: ")
    formattedNewScreeningTime = datetime.strptime(newScreeningTime, "%Y-%m-%d %H:%M")
    insertQuery = "INSERT INTO Screenings (screening_time, movie_id, theater_id) VALUES (%s, %s, %s)"
    newScreeningValues = (
        formattedNewScreeningTime,
        newScreeningMovieID,
        screeningForTheaterID,
    )
    mycursor = mydb.cursor()
    mycursor.execute(insertQuery, newScreeningValues)
    mydb.commit()

    os.system("cls")
    selectQuery = """SELECT S.screening_id, M.movie_name, T.theater_name, S.screening_time
                FROM Screenings AS S
                INNER JOIN Movies AS M ON S.movie_id = M.movie_id 
                INNER JOIN MovieTheaters AS T ON S.theater_id = T.theater_id
                WHERE T.theater_id = %s
                ORDER BY S.screening_time ASC
        """
    val = (screeningForTheaterID,)
    mycursor.execute(selectQuery, val)
    screeningList = mycursor.fetchall()
    print("Screening ID | Movie | Movie Theater | Screening Time")
    for screening in screeningList:
        printLine()
        print(
            str(screening[0])
            + "|"
            + str(screening[1])
            + "|"
            + str(screening[2])
            + "|"
            + screening[3].strftime("%Y-%m-%d %H:%M")
        )

    mycursor.close()
    exit()


def searchMovieTheater():
    flag = True
    while flag:
        theaterName = input("Enter Theater name: ")

        mycursor2 = mydb.cursor()
        sql = "SELECT * FROM MovieTheaters AS M WHERE M.theater_name = %s"
        val = (theaterName,)

        mycursor2.execute(sql, val)
        theater = mycursor2.fetchall()

        if theater:
            flag = False
        else:
            print(red_code + "Incorrect Theater name. Try again." + reset_code)
            printLine()

    print("------", theaterName, "------\n")
    print(" Location: ", theater[0][2])
    print(" Capacity: ", theater[0][3])

    exit()


# If fetch all reteurns 0 items in result set, print no movies currently playing at this time?
def getAllMoviesAtSpecificTheaterSorted():
    mycursor = mydb.cursor()

    flag = True
    while flag:
        theaterName = input("Enter Theater Name: ")

        mycursor2 = mydb.cursor()
        sql = "SELECT theater_id FROM MovieTheaters AS M WHERE M.theater_name = %s"
        val = (theaterName,)

        mycursor2.execute(sql, val)
        theaterID = mycursor2.fetchall()

        if theaterID:
            theaterID = theaterID[0][0]
            flag = False
        else:
            print(red_code + "Incorrect Theater name. Try again." + reset_code)
            printLine()

    sql = """SELECT M.movie_id, M.movie_name, M.release_date, S.screening_time
                FROM Movies AS M
                INNER JOIN Screenings AS S ON M.movie_id = S.movie_id
                INNER JOIN MovieTheaters AS T ON S.theater_id = T.theater_id
                WHERE T.theater_id = %s
                ORDER BY M.release_date DESC
        """

    val = (theaterID,)
    mycursor.execute(sql, val)
    movieList = mycursor.fetchall()

    print(" -----", theaterName, "----- \n")
    for movie in movieList:
        print(" MovieID: ", movie[0])
        print(" Movie Name: ", movie[1])

    exit()


def getAllConcessionsByTheaterName():
    mycursor = mydb.cursor()

    flag = True
    while flag:
        theaterName = input("Enter Theater Name: ")

        mycursor2 = mydb.cursor()
        sql = "SELECT theater_id FROM MovieTheaters AS M WHERE M.theater_name = %s"
        val = (theaterName,)

        mycursor2.execute(sql, val)
        theaterID = mycursor2.fetchall()

        if theaterID:
            theaterID = theaterID[0][0]
            flag = False
        else:
            print(red_code + "Incorrect Theater name. Try again." + reset_code)
            printLine()

    sql = """SELECT C.concession_id, C.snack_name, C.snack_description, C.snack_quantity
            FROM Concessions AS C
            INNER JOIN MovieTheaters AS T ON C.theater_id = T.theater_id
            WHERE T.theater_id = %s

        """

    val = (theaterID,)
    mycursor.execute(sql, val)
    concessionsList = mycursor.fetchall()

    print("------", theaterName, "------\n")
    for concession in concessionsList:
        print("-----", concession[1], "-----")

        print(" Description: ", concession[2])
        print(" Quantity: ", concession[3])

    exit()


# Needs to be wrapped in try catch block incase username doesn't exist
def getAllMovieRatingsByUsername():
    flag = True
    while flag:
        userName = input("Enter the username whose ratings you wish to see: ")
        mycursor = mydb.cursor()
        sql = """SELECT MR.username, MR.rating, M.movie_name
                    FROM MovieRatings AS MR
                    JOIN Movies AS M ON MR.movie_id = M.movie_id
                    WHERE MR.username = %s
            """

        val = (userName,)
        mycursor.execute(sql, val)
        movieRatingsList = mycursor.fetchall()

        if movieRatingsList:
            flag = False
        else:
            print(red_code + "Username does not exist. Try again." + reset_code)
            printLine()

    print("------", userName, "------\n")
    for movieRating in movieRatingsList:
        print(" Movie: ", movieRating[2])
        print(" Rating: ", movieRating[1])
        print("\n")

    exit()


def createRatingForSeenMovie():  # Needs to be edited so that it only shows movies that users have seen, (i.e the booking must be in the past, go through screening id to find which movie the booking is for), need to change dummy data to reflect this requirement
    mycursor = mydb.cursor()
    print("------ Previously Seen Movies ------\n")

    sql = """SELECT M.movie_id, M.movie_name, M.release_date
                FROM Bookings AS B
                JOIN Screenings AS S ON B.booking_screening_id = S.screening_id
                JOIN Movies AS M ON S.screening_id = M.movie_id
                WHERE B.username = %s
                ORDER BY M.release_date DESC
        """
    val = (currentUser[0][0],)
    mycursor.execute(sql, val)
    seenMoviesList = mycursor.fetchall()

    i = 1
    for seenMovie in seenMoviesList:
        print(" -----Movie:", i, "-----")

        print(" Movie Name: ", seenMovie[1])
        print(" Release Date: ", seenMovie[2])

        print("\n")

        i += 1

    movieNum = int(input("Enter the movie number you want to rate: "))
    # Should limit backend to limit rating to be either integer values 1-5
    # Should also not let users leave multiple ratings for the same movie?
    rating = int(input("Enter a rating from 1-5 that you want to give this movie: "))

    mycursor2 = mydb.cursor()
    sql = "INSERT INTO MovieRatings (username, movie_id, rating) VALUES (%s,%s,%s)"
    val = (currentUser[0][0], seenMoviesList[movieNum - 1][0], rating)
    mycursor2.execute(sql, val)
    mydb.commit()
    os.system("cls")

    # output all of this user's movie ratings
    sql = """SELECT MR.username, MR.rating, M.movie_name
                        FROM MovieRatings AS MR
                        JOIN Movies AS M ON MR.movie_id = M.movie_id
                        WHERE MR.username = %s
              """

    val = (currentUser[0][0],)
    mycursor.execute(sql, val)
    movieRatingsList = mycursor.fetchall()

    print("------", currentUser[0][0] + "'s ratings", "------\n")
    for movieRating in movieRatingsList:
        print(" Movie: ", movieRating[2])
        print(" Rating: ", movieRating[1])
        print("\n")

    exit()


def deleteBooking():
    mycursor = mydb.cursor()
    print("------ All Bookings ------\n")
    sql = "SELECT * FROM Bookings WHERE username = %s"
    val = (currentUser[0][0],)
    mycursor.execute(sql, val)
    bookingsList = mycursor.fetchall()

    i = 1
    for booking in bookingsList:
        mycursor2 = mydb.cursor()
        sql = """SELECT M.movie_name, T.theater_name, S.screening_time
                FROM Bookings AS B
                INNER JOIN Screenings AS S ON S.screening_id = B.booking_screening_id
                INNER JOIN Movies AS M ON M.movie_id = S.movie_id
                INNER JOIN MovieTheaters AS T ON T.theater_id = S.theater_id
                WHERE B.booking_id = %s;
        """

        val = (booking[0],)
        mycursor2.execute(sql, val)
        movieBookingList = mycursor2.fetchall()

        print(" -----Booking:", i, "-----")

        print(" Movie: ", movieBookingList[0][0])
        print(" Theater: ", movieBookingList[0][1])
        print(" Time: ", movieBookingList[0][2])

        print("\n")
        i += 1

    # If bookingsList is empty, should not prompt them to drop a booking number and should display "No bookings for (username), and then call exit()?"
    deleteID = int(input("Enter the booking number you want to drop: "))

    mycursor3 = mydb.cursor()
    sql = "DELETE FROM Bookings WHERE booking_id= %s"
    val = (bookingsList[deleteID - 1][0],)
    mycursor3.execute(sql, val)
    mydb.commit()

    os.system("cls")
    print("------ Updated Bookings ------\n")
    sql = "SELECT * FROM Bookings WHERE username = %s"
    val = (currentUser[0][0],)
    mycursor.execute(sql, val)
    updatedBookingsList = mycursor.fetchall()
    i = 1
    for booking in updatedBookingsList:
        mycursor2 = mydb.cursor()
        sql = """SELECT M.movie_name, T.theater_name, S.screening_time
                FROM Bookings AS B
                INNER JOIN Screenings AS S ON S.screening_id = B.booking_screening_id
                INNER JOIN Movies AS M ON M.movie_id = S.movie_id
                INNER JOIN MovieTheaters AS T ON T.theater_id = S.theater_id
                WHERE B.booking_id = %s;
        """

        val = (booking[0],)
        mycursor2.execute(sql, val)
        movieBookingList = mycursor2.fetchall()

        print(" -----Booking:", i, "-----")

        print(" Movie: ", movieBookingList[0][0])
        print(" Theater: ", movieBookingList[0][1])
        print(" Time: ", movieBookingList[0][2])

        print("\n")
        i += 1

    exit()


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
        os.system("cls")
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
            searchMovieTheater()
        elif n == 3:
            os.system("cls")
            getAllMoviesAtSpecificTheaterSorted()
        elif n == 4:
            os.system("cls")
            # insert function here
        elif n == 5:
            os.system("cls")
            # insert function here
        elif n == 6:
            os.system("cls")
            deleteBooking()
        elif n == 7:
            os.system("cls")
            getAllConcessionsByTheaterName()
        elif n == 8:
            os.system("cls")
            getAllMovieRatingsByUsername()
        elif n == 9:
            os.system("cls")
            createRatingForSeenMovie()  # Needs to be edited
        elif n == 10:
            os.system("cls")
            print(" — — — Thank You — — -")
        else:
            os.system("cls")
            displayUserMainMenu()

    else:
        # Admin is logged in
        displayAdminMainMenu()
        n = int(input("Enter option : "))
        if n == 1:
            os.system("cls")  # For Windows
            getAllMovieTheaters()
        elif n == 2:
            os.system("cls")
            searchMovieTheater()
        elif n == 3:
            os.system("cls")
            deleteTheaterByID()
        elif n == 4:
            os.system("cls")
            getAllMoviesAtSpecificTheaterSorted()
        elif n == 5:
            os.system("cls")
            addNewMovie()
        elif n == 6:
            os.system("cls")
            updateMovieByID()
        elif n == 7:
            os.system("cls")
            deleteMovieByID()
        elif n == 8:
            os.system("cls")
            createNewMovieScreening()
        elif n == 9:
            os.system("cls")
            deleteMovieScreeningByID()
        elif n == 10:
            os.system("cls")
            getAllConcessionsByTheaterName()
        elif n == 11:
            os.system("cls")
            print(" — — — Thank You — — -")
        else:
            os.system("cls")
            displayAdminMainMenu()


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
