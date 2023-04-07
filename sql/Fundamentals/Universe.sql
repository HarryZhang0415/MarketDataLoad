CREATE TABLE universe (
  ID INT NOT NULL AUTO_INCREMENT,
  cik INT NOT NULL,
  symbol VARCHAR(20),
  name VARCHAR(200),
  sector VARCHAR(200),
  subSector VARCHAR(200),
  headQuarter VARCHAR(200),
  KEY(ID),
  PRIMARY KEY (cik)
);
