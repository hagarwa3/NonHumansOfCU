CREATE TABLE Users
(
UserID BIGINT AUTO_INCREMENT,
username VARCHAR(30) NULL,
karma BIGINT default 0,
pass VARCHAR(15) NULL,
PRIMARY KEY (UserID));