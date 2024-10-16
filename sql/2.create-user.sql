-- Prompt user for input for the username and password
\prompt 'Enter username: ' username
\prompt 'Enter password: ' password

-- Create the user
CREATE ROLE :username WITH LOGIN PASSWORD :'password';

-- Grant role privileges
GRANT ALL PRIVILEGES ON DATABASE verifix_etl_db TO :username;

-- Create a schema
CREATE SCHEMA IF NOT EXISTS verifix AUTHORIZATION :username;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA verifix TO :username;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA verifix TO :username;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA verifix TO :username;

GRANT USAGE ON SCHEMA verifix TO :username;

ALTER DEFAULT privileges in schema verifix grant all privileges on tables to :username;
ALTER DEFAULT privileges in schema verifix grant all privileges on sequences to :username;
ALTER DEFAULT privileges in schema verifix grant all privileges on functions to :username;