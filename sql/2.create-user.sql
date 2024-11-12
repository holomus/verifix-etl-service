\getenv verifix_db VERIFIX_DB
\getenv verifix_db_user VERIFIX_DB_USER
\getenv verifix_db_password VERIFIX_DB_PASSWORD

\connect :verifix_db

-- Create the user
CREATE ROLE :verifix_db_user WITH LOGIN PASSWORD :'verifix_db_password';

-- Grant role privileges
GRANT ALL PRIVILEGES ON DATABASE :verifix_db TO :verifix_db_user;

-- Create a schema
CREATE SCHEMA IF NOT EXISTS :verifix_db_user AUTHORIZATION :verifix_db_user;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA :verifix_db_user TO :verifix_db_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA :verifix_db_user TO :verifix_db_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA :verifix_db_user TO :verifix_db_user;

GRANT USAGE ON SCHEMA :verifix_db_user TO :verifix_db_user;

ALTER DEFAULT privileges in schema :verifix_db_user grant all privileges on tables to :verifix_db_user;
ALTER DEFAULT privileges in schema :verifix_db_user grant all privileges on sequences to :verifix_db_user;
ALTER DEFAULT privileges in schema :verifix_db_user grant all privileges on functions to :verifix_db_user;