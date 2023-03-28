USE utils;
CREATE TABLE DataProvider (
    ProviderID int NOT NULL AUTO_INCREMENT,
    ProviderName varchar(255),
    ProviderAbbrev varchar(255),
    API_Key varchar(255),
    PRIMARY KEY (ProviderID)
);