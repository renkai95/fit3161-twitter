-- SELECT * FROM twitter.harvey_cleaned;
SHOW VARIABLES LIKE "secure_file_priv";
truncate table harvey_cleaned;
LOAD DATA INFILE 'D:\DATA\\test.csv' 
INTO TABLE harvey_cleaned 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '|'
ESCAPED BY ''
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;