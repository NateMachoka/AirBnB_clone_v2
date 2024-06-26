-- Prepare a MySQL server for the project
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a new user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'
IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on database
GRANT ALL PRIVILEGES ON hbnb_test_db . * TO 'hbnb_test'@'localhost';

-- Grant select privileges performance schema
GRANT SELECT ON performance_schema . * TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
