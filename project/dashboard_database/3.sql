DROP TABLE IF EXISTS `BOOK`;

CREATE TABLE BOOK(
	BOOKID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	BNAME VARCHAR(100) DEFAULT '' NOT NULL,
	NUMBER_OF_CHAPTERS INT DEFAULT 0 NOT NULL,
	NUMBER_OF_EXERCISES INT DEFAULT 0 NOT NULL
);

INSERT INTO BOOK (BNAME, NUMBER_OF_CHAPTERS, NUMBER_OF_EXERCISES) VALUES 
('Introduction to Programming', 10, 200),
('Data Structures and Algorithms', 12, 250),
('Database Systems', 8, 150),
('Computer Networks', 9, 180),
('Web Development', 7, 120),
('Operating Systems', 11, 220),
('Artificial Intelligence', 13, 280),
('Computer Graphics', 6, 100),
('Software Engineering', 9, 180),
('Cybersecurity', 10, 200);