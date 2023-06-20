DROP TABLE IF EXISTS `INSTRUCTOR`;

CREATE TABLE INSTRUCTOR(
	INSTID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	IFIRST_NAME VARCHAR(50) NOT NULL,
	ILAST_NAME VARCHAR(50) NOT NULL,
	IPHONE_NUMBER VARCHAR(20) NOT NULL,
	IEMAIL VARCHAR(255) NOT NULL,
	ICOUNTRY VARCHAR(30) NOT NULL,
	CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO INSTRUCTOR (IFIRST_NAME, ILAST_NAME, IPHONE_NUMBER, IEMAIL, ICOUNTRY) VALUES 
('John', 'Doe', '+123456789', 'john.doe@gmail.com', 'USA'),
('Jane', 'Doe', '+123456789', 'jane.doe@gmail.com', 'USA'),
('Mark', 'Smith', '+123456789', 'mark.smith@gmail.com', 'Canada'),
('Lisa', 'Lee', '+123456789', 'lisa.lee@gmail.com', 'South Korea'),
('David', 'Kim', '+123456789', 'david.kim@gmail.com', 'South Korea'),
('Anna', 'Wong', '+123456789', 'anna.wong@gmail.com', 'Hong Kong'),
('Tom', 'Li', '+123456789', 'tom.li@gmail.com', 'China'),
('Maria', 'Garcia', '+123456789', 'maria.garcia@gmail.com', 'Spain'),
('Pedro', 'Gonzalez', '+123456789', 'pedro.gonzalez@gmail.com', 'Mexico'),
('Emilie', 'Dubois', '+123456789', 'emilie.dubois@gmail.com', 'France');