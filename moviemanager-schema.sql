DROP DATABASE IF EXISTS sampleDB;
CREATE DATABASE sampleDB;
USE sampleDB;



 CREATE TABLE Customers (
	username VARCHAR(50) NOT NULL,
	password VARCHAR(100) NOT NULL,
	location VARCHAR(250) NOT NULL, 
	PRIMARY KEY (username)
    
);

CREATE TABLE Administrators (
            username VARCHAR(50) NOT NULL,
            password VARCHAR(100) NOT NULL,
            date_joined DATE NOT NULL,
            PRIMARY KEY (username)
);

CREATE TABLE MovieTheaters (
            theater_id INT AUTO_INCREMENT,
            theater_name VARCHAR(100) NOT NULL,
            theater_location VARCHAR(150) NOT NULL,
            max_seating_capacity INT NOT NULL,
            PRIMARY KEY (theater_id)
);

CREATE TABLE Movies (
            movie_id INT AUTO_INCREMENT,
            movie_name VARCHAR(100) NOT NULL,
            movie_description VARCHAR(500) NOT NULL,
            release_date DATE NOT NULL,
            PRIMARY KEY (movie_id)
);


CREATE TABLE Screenings (
            screening_id INT AUTO_INCREMENT,
            screening_time DATETIME NOT NULL,
            movie_id INT NOT NULL,
            theater_id INT NOT NULL,
            PRIMARY KEY (screening_id, screening_time),
            FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
			FOREIGN KEY (theater_id) REFERENCES MovieTheaters(theater_id) ON DELETE CASCADE
);

CREATE INDEX idx_time
ON Screenings (screening_time);

CREATE TABLE Bookings (
    booking_id INT AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    booking_screening_id INT NOT NULL,
    booking_time DATETIME NOT NULL,
    PRIMARY KEY (booking_id),
    FOREIGN KEY (username) REFERENCES Customers(username) ON DELETE CASCADE,
    FOREIGN KEY (booking_screening_id) REFERENCES Screenings(screening_id) ON DELETE CASCADE,
    FOREIGN KEY (booking_time) REFERENCES Screenings(screening_time) ON UPDATE CASCADE
);

CREATE TABLE MovieRatings (
    rating_id INT AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    movie_id INT NOT NULL,
    rating INT NOT NULL,
    PRIMARY KEY (rating_id, username, movie_id),
    FOREIGN KEY (username) REFERENCES Customers(username) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE
);
CREATE TABLE Concessions (
    concession_id INT AUTO_INCREMENT,
    snack_name VARCHAR(100) NOT NULL,
    snack_description VARCHAR(250) NOT NULL,
    snack_quantity INT NOT NULL,
    theater_id INT NOT NULL,
    PRIMARY KEY (concession_id, theater_id),
    FOREIGN KEY (theater_id) REFERENCES MovieTheaters(theater_id)
);
CREATE TABLE PromotionalDiscounts (
    promo_id INT AUTO_INCREMENT,
    promo_description VARCHAR(250) NOT NULL,
    discount DECIMAL(3,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    discounted_theater_id INT NOT NULL,
    PRIMARY KEY (promo_id),
	FOREIGN KEY (discounted_theater_id) REFERENCES MovieTheaters(theater_id)
	ON DELETE CASCADE
        );

INSERT INTO Customers (`username`,`password`,`location`) VALUES 
   ('Briar245','tuMls&+ch3guwihoFrep','New York City'),
   ('OptimusPr1m3','*+Truy&WlxidR&M10RuV','Seattle'),
   ('Shivana24143','sWiwRat&iV&WE0roMANU','Philadelphia'),
   ('JoeMamma456','#o-ezeH@wu2hu17A2iZ&','Lancaster'),
   ('GodCr1Tic2345','b7wrich#Xas_iwab5lri','Newark');

INSERT INTO Administrators (`username`,`password`,`date_joined`) VALUES 
   ('CrisperPluto251','C=Wlfre9ec?zazLClwis','1997-12-04'),
   ('Marauder23','chubr*5ro1RestewRlfE','2002-09-17'),
   ('3R3NJaeguer234','chubr*5ro1RestewRlfE','2000-08-19'),
   ('AceEater34','siri@eX?272?esib@p*u','1999-10-18'),
   ('Yallah2591','kopAST6+?v$6!wrE&aPR','1995-04-29');

INSERT INTO MovieTheaters  VALUES 
   (1,'Regal Cinema','Lancaster', 300),
   (2,'Dreamland Cinemas','Seattle', 400),
   (3,'Harmony Picture Palace','Palo Alto', 150),
   (4,'Silver Screen Showcase','Las Vegas', 200),
   (5,'Grand Horizon Theatres','Washington D.C', 200);

INSERT INTO Movies(`movie_id`,`movie_name`,`movie_description`, `release_date`)  VALUES 
   (1,'Inception',"A mind-bending thriller where skilled thieves enter peoples 
		dreams to steal their deepest secrets", '2010-10-07'),
   (2,'The Shawshank Redemption','The tale of resilience and friendship unfolds as a banker is wrongly 
			convicted of murder and adapts to life in Shawshank State Penitentiary','1994-03-09'),
   (3,'The Dark Knight',"The Caped Crusader faces his most formidable foe, 
	the Joker, in a gritty and intense battle for Gotham City's soul.",'2008-06-07'),
   (4,'Forrest Gump','A heartwarming journey through decades of American history as witnessed by a simple-minded 
		yet extraordinary man named Forrest Gump','1994-06-07'),
   (5,'Pulp Fiction',"Quentin Tarantino's non-linear narrative weaves together crime, humor, 
		and unexpected twists in the interconnected lives of various characters",'1994-10-05');
   
INSERT INTO Screenings VALUES 
	(1,'2023-12-05 20:00:00',2,3),
	(2,'2023-12-05 22:00:00',4,1),
	(3,'2023-12-04 18:45:00',5,1),
	(4,'2023-12-08 19:00:00',1,4),
	(5,'2023-12-03 21:30:00',5,2);
   

INSERT INTO Bookings(`booking_id`,`username`,`booking_screening_id`, `booking_time`) VALUES 
   (1, 'OptimusPr1m3', 2, '2023-12-05 22:00:00'),
   (2, 'GodCr1Tic2345', 4, '2023-12-08 19:00:00'),
   (3, 'JoeMamma456', 5, '2023-12-03 21:30:00'),
   (4, 'Shivana24143', 1,'2023-12-05 20:00:00'),
   (5, 'GodCr1Tic2345', 5, '2023-12-03 21:30:00');

INSERT INTO MovieRatings(`rating_id`,`username`,`movie_id`, `rating`) VALUES 
   (1, 'JoeMamma456', 3, 3),
   (2, 'OptimusPr1m3', 2, 5),
   (3, 'OptimusPr1m3', 4, 4),
   (4, 'GodCr1Tic2345', 1, 2),
   (5, 'GodCr1Tic2345', 5, 5);
   

   INSERT INTO Concessions(`concession_id`,`snack_name`,`snack_description`, `snack_quantity`, `theater_id`) VALUES 
   (1, 'Popcorn', 'Classic buttered popcorn', 100, 1),
   (2, 'Soda', 'Large cola with ice', 75, 1),
   (3, 'Candy', 'Assorted candy pack', 50, 1),
   (4, 'Nachos', 'Cheesy nachos with salsa', 60, 2),
   (5, 'Ice Cream', 'Vanilla and chocolate swirl', 40, 2);

INSERT INTO PromotionalDiscounts(`promo_id`,`promo_description`,`discount`, `start_date`, `end_date`, `discounted_theater_id`) VALUES 
   (1, 'Early Bird Special', '0.15', '2023-01-15', '2023-02-15', 1),
   (2, 'Family Movie Night', '0.20', '2023-03-01', '2023-03-31', 2),
   (3, 'Student Discount', '0.10', '2023-02-01', '2023-02-28', 3),
   (4, 'Date Night Package', '0.25', '2023-01-20', '2023-02-20', 1),
   (5, 'Senior Citizen Discount', '0.15', '2023-02-10', '2023-03-10', 2);

INSERT INTO MovieTheaters(`theater_name`,`theater_location`,`max_seating_capacity`) VALUES 
	('Cinemark','Dickson City', 420);

SELECT * FROM Customers;
SELECT * FROM MovieTheaters;

