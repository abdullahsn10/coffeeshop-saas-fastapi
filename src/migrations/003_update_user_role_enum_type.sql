-- Create a new ENUM type with uppercase values
CREATE TYPE user_role_upper AS ENUM ('CASHIER', 'CHEF', 'ORDER_RECEIVER', 'ADMIN');

-- Update the users table to use the new ENUM type
ALTER TABLE users ALTER COLUMN role TYPE user_role_upper USING role::text::user_role_upper;

--Drop the old ENUM type
DROP TYPE user_role;

--Rename the new ENUM type to the original name
ALTER TYPE user_role_upper RENAME TO user_role;
