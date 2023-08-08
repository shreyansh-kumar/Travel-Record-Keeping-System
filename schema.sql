DROP TABLE IF EXISTS payment_info;
DROP TABLE IF EXISTS expense_info;
DROP TABLE IF EXISTS travel_info;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS login;






CREATE TABLE login (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  position_id INTEGER NOT NULL
);



CREATE TABLE employee (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    dob INTEGER NOT NULL,
    start_date INTEGER NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    ssn INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (id) REFERENCES login(id)
);



CREATE TABLE travel_info (
    id INTEGER,
    mode VARCHAR(255) NOT NULL,
    booking_id INTEGER UNIQUE NOT NULL,
    ticket_num INTEGER,
    date_dep INTEGER NOT NULL,
    date_arr INTEGER NOT NULL,
    travel_time INTEGER,
    PRIMARY KEY (id, booking_id),
    FOREIGN KEY (id) REFERENCES employee(id)

);



CREATE TABLE expense_info (
    id INTEGER,
    booking_id INTEGER NOT NULL,
    cost INTEGER NOT NULL,
    paid TINYINT NOT NULL,
    PRIMARY KEY (id, booking_id), 
    FOREIGN KEY (id) REFERENCES employee(id),
    FOREIGN KEY (booking_id) REFERENCES travel_info(booking_id)
);



CREATE TABLE payment_info (
    id INTEGER PRIMARY KEY,
    acc_num INTEGER UNIQUE NOT NULL,
    route_num INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES employee(id)
);

/*
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'verybdpassword'
CREATE USER 'HR'@'localhost' IDENTIFIED BY 'verybdpassword'
CREATE USER 'acc'@'localhost' IDENTIFIED BY 'verybdpassword'
CREATE USER 'emp'@'localhost' IDENTIFIED BY 'verybdpassword'


GRANT ALL ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
GRANT ALL ON *.* TO 'HR'@'localhost';
*/