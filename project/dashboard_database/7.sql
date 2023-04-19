DROP TABLE IF EXISTS `CHAPTER`;

CREATE TABLE CHAPTER(
	CHID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	CHNAME VARCHAR(100) NOT NULL,
	NUMBER_OF_SECTIONS INT,
	NUMBER_OF_EXERCISES INT,
	BOOKID INT,
	FOREIGN KEY (BOOKID) REFERENCES BOOK(BOOKID)
);

INSERT INTO CHAPTER (CHNAME, NUMBER_OF_SECTIONS, NUMBER_OF_EXERCISES, BOOKID) VALUES
('Introduction', 5, 20, 1),
('Variables and Data Types', 7, 25, 1),
('Control Structures', 10, 35, 1),
('Functions', 8, 20, 1),
('Arrays', 6, 20, 1),
('Pointers', 4, 15, 1),
('Recursion', 5, 15, 1),
('Sorting and Searching', 9, 25, 1),
('Object-Oriented Programming', 10, 30, 1),
('Exception Handling', 6, 15, 1),
('Data Structures', 7, 25, 2),
('Algorithm Analysis', 8, 30, 2),
('Trees', 9, 35, 2),
('Graphs', 10, 40, 2),
('Sorting Algorithms', 6, 20, 2),
('Searching Algorithms', 7, 25, 2),
('Hashing', 5, 15, 2),
('Dynamic Programming', 8, 30, 2),
('Database Design', 7, 25, 3),
('SQL Queries', 8, 30, 3),
('Database Administration', 6, 20, 3),
('Database Programming', 7, 25, 3),
('Networking Fundamentals', 7, 25, 4),
('TCP/IP Protocol Suite', 8, 30, 4),
('Network Security', 8, 25, 4),
('Wireless Networks', 6, 20, 4),
('HTML', 5, 15, 5),
('CSS', 5, 15, 5),
('JavaScript', 7, 25, 5),
('Web Development Frameworks', 5, 20, 5),
('Process Management', 8, 25, 6),
('Memory Management', 8, 30, 6),
('File Systems', 7, 25, 6),
('Device Drivers', 8, 30, 6),
('Search Algorithms', 7, 25, 6),
('Introduction to AI', 6, 20, 7),
('Search Algorithms in AI', 7, 25, 7),
('Knowledge Representation', 8, 30, 7),
('Expert Systems', 7, 25, 7),
('Neural Networks', 9, 35, 7),
('Genetic Algorithms', 6, 20, 7),
('Rendering Techniques', 7, 25, 8),
('3D Modeling', 6, 20, 8),
('Animation', 5, 15, 8),
('Virtual Reality', 7, 25, 8),
('Software Requirements', 7, 25, 9),
('Software Design', 8, 30, 9),
('Software Testing', 7, 25, 9),
('Software Maintenance', 8, 30, 9),
('Agile Methodologies', 9, 35, 9),
('Security Principles', 6, 20, 10),
('Cryptography', 8, 30, 10),
('Network Security', 8, 25, 10),
('Threat Modeling', 6, 20, 10);