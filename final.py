import mysql.connector
import os
import getpass


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




def getAllMovieTheaters():
    
    mycursor = mydb.cursor()
    print('------ All Theaters ------\n')
    mycursor.execute("SELECT * FROM MovieTheaters")
    theatherList = mycursor.fetchall()

    
    for theater in theatherList:
        
        print(" -----", theater[1], "-----")

        
       
        print(" Location : ", theater[2])
        print(" Capacity : ", theater[3])
        
        print("\n")

    print('------ SUCCESS ------\n')
    exit()

def searchMovieTheater():
    
    
    flag = True
    while flag:

        theaterName = input("Enter Theater Name: ")
        

        mycursor2 = mydb.cursor()
        sql = "SELECT * FROM MovieTheaters AS M WHERE M.theater_name = %s"
        val = (theaterName,)
        
        mycursor2.execute(sql,val)
        theater = mycursor2.fetchall()
       
        if theater:
            
            flag = False
        else:
            print("Incorrect Theater name. Try again.")
            printLine()

    

    print("------", theaterName, "------\n")
    print(" Location : ", theater[0][2])
    print(" Capacity : ", theater[0][3])
        
    print("\n")

    
    print('------ SUCCESS ------\n')
    exit()

def getAllMoviesAtSpecificTheater():
    
    mycursor = mydb.cursor()
    
    flag = True
    while flag:

        theaterName = input("Enter Theater Name: ")
        

        mycursor2 = mydb.cursor()
        sql = "SELECT theater_id FROM MovieTheaters AS M WHERE M.theater_name = %s"
        val = (theaterName,)
        
        mycursor2.execute(sql,val)
        theaterID = mycursor2.fetchall()
       
        if theaterID:
            theaterID = theaterID[0][0]
            flag = False
        else:
            print("Incorrect Theater name. Try again.")
            printLine()

    

    sql = """SELECT DISTINCT M.movie_id, M.movie_name
            FROM Movies AS M
            INNER JOIN Screenings S ON M.movie_id = S.movie_id
            WHERE S.theater_id = %s
        """
 
    val = (theaterID,)
    mycursor.execute(sql,val)
    movieList = mycursor.fetchall()

    print("------", theaterName, "------\n")
    for movie in movieList:
        
        
        print(" MoiveID : ", movie[0])
        print(" Movie Name : ", movie[1])
        
        print("\n")

    print('------ SUCCESS ------\n')
    exit()

def getAllMoviesAtSpecificTheaterSorted():
    
    mycursor = mydb.cursor()
    
    flag = True
    while flag:

        theaterName = input("Enter Theater Name: ")
        

        mycursor2 = mydb.cursor()
        sql = "SELECT theater_id FROM MovieTheaters AS M WHERE M.theater_name = %s"
        val = (theaterName,)
        
        mycursor2.execute(sql,val)
        theaterID = mycursor2.fetchall()
       
        if theaterID:
            theaterID = theaterID[0][0]
            flag = False
        else:
            print("Incorrect Theater name. Try again.")
            printLine()

    



    
    sql = """SELECT M.movie_id, M.movie_name, M.release_date, S.screening_time
                FROM Movies AS M
                INNER JOIN Screenings AS S ON M.movie_id = S.movie_id
                INNER JOIN MovieTheaters AS T ON S.theater_id = T.theater_id
                WHERE T.theater_id = %s
                ORDER BY M.release_date DESC
        """
 
    val = (theaterID,)
    mycursor.execute(sql,val)
    movieList = mycursor.fetchall()

    print(" -----", theaterName, "----- \n")
    for movie in movieList:
        
        
        print(" MoiveID : ", movie[0])
        print(" Movie Name : ", movie[1])
        
        print("\n")

    print('------ SUCCESS ------\n')
    exit()

def getAllConcessions():
    
    mycursor = mydb.cursor()
    
    flag = True
    while flag:

        theaterName = input("Enter Theater Name: ")
        

        mycursor2 = mydb.cursor()
        sql = "SELECT theater_id FROM MovieTheaters AS M WHERE M.theater_name = %s"
        val = (theaterName,)
        
        mycursor2.execute(sql,val)
        theaterID = mycursor2.fetchall()
       
        if theaterID:
            theaterID = theaterID[0][0]
            flag = False
        else:
            print("Incorrect Theater name. Try again.")
            printLine()

    

    sql = """SELECT C.concession_id, C.snack_name, C.snack_description, C.snack_quantity
            FROM Concessions AS C
            INNER JOIN MovieTheaters AS T ON C.theater_id = T.theater_id
            WHERE T.theater_id = %s

        """
 
    val = (theaterID,)
    mycursor.execute(sql,val)
    concessionsList = mycursor.fetchall()

    print("------", theaterName, "------\n")
    for concession in concessionsList:
        
        print("-----", concession[1], "-----")

        
       
        print(" Description : ", concession[2])
        print(" Quantity : ", concession[3])
        


    print('------ SUCCESS ------\n')
    exit()

def getAllMovieRatings():
    
    flag = True
    while flag:

        userName = input("Enter User Name: ")
        mycursor = mydb.cursor()
        sql = """SELECT MR.username, MR.rating, M.movie_name
                    FROM MovieRatings AS MR
                    JOIN Movies AS M ON MR.movie_id = M.movie_id
                    WHERE MR.username = %s
            """
    
        val = (userName,)
        mycursor.execute(sql,val)
        movieRatingsList = mycursor.fetchall()
        
       
        if movieRatingsList:
            flag = False
        else:
            print("Incorrect User name. Try again.")
            printLine()

    


    print("------", userName, "------\n")
    for movieRating in movieRatingsList:
        
        
        print(" Moive : ", movieRating[2])
        print(" Rating : ", movieRating[1])
        
        print("\n")

    print('------ SUCCESS ------\n')
    exit()

def getAllMoviesAtSpecificTheaterSorted():
    
    mycursor = mydb.cursor()
    
    flag = True
    while flag:

        theaterName = input("Enter Theater Name: ")
        

        mycursor2 = mydb.cursor()
        sql = "SELECT theater_id FROM MovieTheaters AS M WHERE M.theater_name = %s"
        val = (theaterName,)
        
        mycursor2.execute(sql,val)
        theaterID = mycursor2.fetchall()
       
        if theaterID:
            theaterID = theaterID[0][0]
            flag = False
        else:
            print("Incorrect Theater name. Try again.")
            printLine()

    



    
    sql = """SELECT M.movie_id, M.movie_name, M.release_date, S.screening_time
                FROM Movies AS M
                INNER JOIN Screenings AS S ON M.movie_id = S.movie_id
                INNER JOIN MovieTheaters AS T ON S.theater_id = T.theater_id
                WHERE T.theater_id = %s
                ORDER BY M.release_date DESC
        """
 
    val = (theaterID,)
    mycursor.execute(sql,val)
    movieList = mycursor.fetchall()

    print(" -----", theaterName, "----- \n")
    for movie in movieList:
        
        
        print(" MoiveID : ", movie[0])
        print(" Movie Name : ", movie[1])
        
        print("\n")

    print('------ SUCCESS ------\n')
    exit()


def bookTicket():

    mycursor = mydb.cursor()
    
    flag = True
    while flag:

        theaterName = input("Enter Theater Name: ")
        

        mycursor2 = mydb.cursor()
        sql = "SELECT theater_id FROM MovieTheaters AS M WHERE M.theater_name = %s"
        val = (theaterName,)
        
        mycursor2.execute(sql,val)
        theaterID = mycursor2.fetchall()
       
        if theaterID:
            theaterID = theaterID[0][0]
            flag = False
        else:
            print("Incorrect Theater name. Try again.")
            printLine()

    
    print('------ Avaiable Screenings ------\n')

    sql = "SELECT * FROM Screenings WHERE theater_id = %s"
    val = (theaterID,)
    mycursor.execute(sql,val)
    screeningList = mycursor.fetchall()

    i = 1
    for screening in screeningList:
        print('------ Screening', i ,' ------\n')
        mycursor3 = mydb.cursor()
        sql = "SELECT movie_name FROM Movies AS M WHERE M.movie_id = %s"
        val = (screening[2],)
        
        mycursor3.execute(sql,val)
        movie = mycursor.fetchall()

        print("Movie: ", movie[0][0])
        print("Movie Screening Time : ", screening[1])
        
        print("\n")
        i +=1

    screeningNum = int(input('Enter the screening number you want to book: '))



    mycursor4 = mydb.cursor()
    sql = "INSERT INTO Bookings (username,booking_screening_id, booking_time) VALUES (%s,%s,%s)"
    val = (currentUser[0][0], screeningList[screeningNum-1][0],screeningList[screeningNum-1][1])
    mycursor4.execute(sql,val)
    mydb.commit()

    print('------ SUCCESS ------\n')
    exit()



def deleteBooking():
    
    mycursor = mydb.cursor()
    print('------ All Bookings ------\n')
    sql = "SELECT * FROM Bookings WHERE username = %s"
    val = (currentUser[0][0],)
    mycursor.execute(sql,val)
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
        mycursor2.execute(sql,val)
        movieBookingList = mycursor2.fetchall()
 
        
        print(" -----Booking:", i, "-----")

        
        print(" Movie : ", movieBookingList[0][0])
        print(" Theater : ", movieBookingList[0][1])
        print(" Time : ", movieBookingList[0][2])
        
        print("\n")
        i+=1

    deleteID = int(input('Enter the booking number you want to drop: '))

    mycursor3 = mydb.cursor()
    sql = "DELETE FROM Bookings WHERE booking_id= %s"
    val = (bookingsList[deleteID-1][0],)
    mycursor3.execute(sql,val)
    mydb.commit()
    

    print('------ SUCCESS ------\n')
    exit()

def ratingMovies():
    
    mycursor = mydb.cursor()
    print('------ All Movies ------\n')
    mycursor.execute("SELECT * FROM Movies")
    movieList = mycursor.fetchall()

    i = 1
    for movie in movieList:
        
        print(" -----Movie:", i, "-----")

        
        print(" Movie Name : ", movie[1])
        print(" Description : ", movie[2])
        print(" Release Date : ", movie[3])
        
        print("\n")

        i +=1

    movieNum = int(input('Enter the movie number you want to rate: '))
    rating = int(input('Enter the rating you want to give this movie: '))



    mycursor2 = mydb.cursor()
    sql = "INSERT INTO MovieRatings (username, movie_id, rating) VALUES (%s,%s,%s)"
    val = (currentUser[0][0], movieList[movieNum-1][0],rating)
    mycursor2.execute(sql,val)
    mydb.commit()

    print('------ SUCCESS ------\n')
    exit()



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
    printLine()


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
    else:
        # os.system("cls")
        run()

    if not adminLoggedIn:
        # User is logged in
        displayUserMainMenu()
        n = int(input("Enter option : "))
        if n == 1:
        #     os.system("cls")  # For Windows
            getAllMovieTheaters()
        elif n == 2:
        #     os.system("cls")
            searchMovieTheater()
        elif n == 3:
        #     os.system("cls")
           
            getAllMoviesAtSpecificTheater()
        elif n == 4:
            getAllMoviesAtSpecificTheaterSorted()
        #     os.system("cls")
        elif n == 6:
            bookTicket()
        elif n == 7:
            deleteBooking()
        elif n == 8:
            getAllConcessions()
        elif n == 9:
            getAllMovieRatings()
        elif n == 10:
            ratingMovies()
        #     print(" — — — Thank You — — -")
        # else:
        #     # os.system("cls")
        #     run()

    else:
        # Admin is logged in
        displayAdminMainMenu()
        # n = int(input("Enter option : "))
        # if n == 1:
        #     os.system("cls")  # For Windows
        #     userLogin()
        # elif n == 2:
        #     os.system("cls")
        #     adminLogin()
        # elif n == 3:
        #     os.system("cls")
        #     print(" — — — Thank You — — -")
        # else:
        #     # os.system("cls")
        #     run()


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