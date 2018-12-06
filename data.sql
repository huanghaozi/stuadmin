CREATE TABLE department (
  departid CHAR(2) PRIMARY KEY NOT NULL,
  departname CHAR(20) NOT NULL,
  departhead CHAR(8),
  telephone CHAR(13)
);

CREATE TABLE class (
  class CHAR(6) PRIMARY KEY NOT NULL,
  classname CHAR(20) NOT NULL,
  departid CHAR(2) NOT NULL,
  begindate DATE NOT NULL,
  master CHAR(8),
  matertel CHAR(13),
  FOREIGN KEY(departid) REFERENCES department(departid)
);

CREATE TABLE student (
  studentid CHAR(8) PRIMARY KEY NOT NULL,
  name CHAR(8) NOT NULL,
  sex CHAR(2) NOT NULL,
  classid CHAR(6) NOT NULL,
  birthday DATE,
  native CHAR(16),
  FOREIGN KEY(classid) REFERENCES class(classid)
);

CREATE TABLE change (
  cid INTEGER AUTOINCREMENT PRIMARY KEY NOT NULL,
  studentid CHAR(8) NOT NULL,
  change CHAR(4) NOT NULL,
  recdate DATE NOT NULL,
  FOREIGN KEY(studentid) REFERENCES student(studentid)
);

CREATE TABLE reward (
  rid INTEGER AUTOINCREMENT PRIMARY KEY NOT NULL,
  studentid CHAR(8) NOT NULL,
  reward CHAR(20) NOT NULL,
  recdate DATE NOT NULL,
  FOREIGN KEY(studentid) REFERENCES student(studentid)
);

CREATE TABLE punish (
  pid INTEGER AUTOINCREMENT PRIMARY KEY NOT NULL,
  studentid CHAR(8) NOT NULL,
  punish CHAR(4) NOT NULL,
  recdate DATE NOT NULL,
  FOREIGN KEY(studentid) REFERENCES student(studentid)
);