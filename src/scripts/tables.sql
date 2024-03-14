-- Create custom Citext domain used for email validity constraints. Emails are case-insensitive and match the provided regex
CREATE EXTENSION citext;
CREATE DOMAIN  domain_email AS citext
CHECK(
   VALUE ~ '^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
);


CREATE TABLE records (
    id SERIAL PRIMARY KEY,
    email domain_email UNIQUE,
    text VARCHAR(100)
);