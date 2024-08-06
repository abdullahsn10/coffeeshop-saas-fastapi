-- update users table (phone_number -> phone_no)
ALTER TABLE users RENAME COLUMN phone_number TO phone_no;
