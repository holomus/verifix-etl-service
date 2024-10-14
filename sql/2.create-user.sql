-- Prompt user for input for the username and password
\prompt 'Enter username: ' username
\prompt 'Enter password: ' password

-- Create the user
CREATE ROLE :username WITH LOGIN PASSWORD :'password';

-- Grant role privileges
GRANT ALL PRIVILEGES ON DATABASE verifix_etl_db TO :username;

-- Create a schema
CREATE SCHEMA IF NOT EXISTS verifix AUTHORIZATION :username;