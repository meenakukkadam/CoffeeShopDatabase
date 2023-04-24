CREATE TABLE products (
	productID varchar(10) PRIMARY KEY,
	productname varchar(60),
	price DECIMAL(10,2),
	productcost DECIMAL(10,2),
	stock integer
);

CREATE TABLE owners (
	ownerID integer PRIMARY KEY,
	fName varchar(30),
	lName varchar(30),
	ownAddress varchar(50),
	email varchar(30),
	DOB date,
	phoneNumber bigint
);

CREATE TABLE shop (
	shopID integer PRIMARY KEY,
	supplierID integer,
	shopLocation varchar(30),
	ownerID integer NOT NULL REFERENCES owners,
	revenue integer
);

CREATE TABLE customer (
	customerID char(10) PRIMARY KEY,
	passw varchar(30),
	fName varchar(30),
	lName varchar(30),
	customerAddress varchar(50),
	email varchar(30),
	DOB date,
	phoneNumber bigint,
	balance decimal(10,2)
);

CREATE TABLE employees (
	ssn integer PRIMARY KEY,
	fName varchar(30),
	lName varchar(30),
	empAddress varchar(50),
	email varchar(30),
	DOB date,
	phoneNumber bigint,
	storeID integer REFERENCES shop,
	passw varchar(30)
);

CREATE TABLE managers (
	managerID integer PRIMARY KEY REFERENCES employees ON DELETE CASCADE
);

CREATE TABLE cashiers (
	empID integer PRIMARY KEY REFERENCES employees ON DELETE CASCADE,
	manager integer REFERENCES managers
);

CREATE TABLE barista (
	empID integer PRIMARY KEY REFERENCES employees ON DELETE CASCADE,
	manager integer REFERENCES managers
);

CREATE TABLE orders (
    orderID integer PRIMARY KEY,
    customerID char(10) NOT NULL REFERENCES customer ON DELETE CASCADE,
    storeID integer NOT NULL REFERENCES shop ON DELETE CASCADE,
    dates DATE,
    totalPrice DECIMAL(10,2),
	cashierID integer REFERENCES cashiers,
	baristaID integer NOT NULL REFERENCES barista
);

CREATE TABLE contain (
	OrID integer REFERENCES orders,
	PrID varchar(10) REFERENCES products,
	quantity integer,
	CONSTRAINT contains_pk PRIMARY KEY(OrID, PrID)
);

CREATE TABLE employs (
	empID integer REFERENCES employees,
	ownerID integer REFERENCES owners,
	salary DECIMAL(10,2),
	CONSTRAINT employs_pk PRIMARY KEY(empID, ownerID)
);