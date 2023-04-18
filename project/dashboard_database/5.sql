DROP TABLE IF EXISTS `STUDENT`;

CREATE TABLE STUDENT(
	SID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	SFIRST_NAME VARCHAR(50) NOT NULL,
	SLAST_NAME VARCHAR(50) NOT NULL,
	SPHONE_NUMBER VARCHAR(20),
	SEMAIL VARCHAR(255) NOT NULL,
	SCOUNTRY VARCHAR(30),
	CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO STUDENT (SFIRST_NAME, SLAST_NAME, SPHONE_NUMBER, SEMAIL, SCOUNTRY) VALUES
('John', 'Doe', '+1-555-1234', 'johndoe@example.com', 'USA'),
('Jane', 'Smith', '+44-20-1234-5678', 'janesmith@example.com', 'UK'),
('Ali', 'Khan', '+92-300-1234567', 'alikhan@example.com', 'Pakistan'),
('Maria', 'Garcia', '+34-91-123-4567', 'mariagarcia@example.com', 'Spain'),
('Hiroshi', 'Tanaka', '+81-3-1234-5678', 'hiroshit@example.com', 'Japan'),
('Marta', 'Petrovic', '+381-11-1234-567', 'martapetrovic@example.com', 'Serbia'),
('Sofia', 'Fernandez', '+54-11-1234-5678', 'sofiafernandez@example.com', 'Argentina'),
('Mustafa', 'Ali', '+20-122-1234567', 'mustafaali@example.com', 'Egypt'),
('Gabriela', 'Silva', '+55-21-1234-5678', 'gabrielasilva@example.com', 'Brazil'),
('Chen', 'Wei', '+86-10-1234-5678', 'chenwei@example.com', 'China');
