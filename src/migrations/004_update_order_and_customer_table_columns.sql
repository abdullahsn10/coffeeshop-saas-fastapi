-- Add assigner_id column to the order table, allowing NULL values
ALTER TABLE "order"
ADD COLUMN assigner_id INT NULL,
ADD FOREIGN KEY (assigner_id) REFERENCES "user"(id) ON DELETE RESTRICT;

-- Add status column to the order table
ALTER TABLE "order"
ADD COLUMN status VARCHAR(50); -- Adjust the length as needed

-- Rename employee_id column to issuer_id
ALTER TABLE "order"
RENAME COLUMN employee_id TO issuer_id;

-- Create the enum type
CREATE TYPE order_status AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CLOSED');

-- Alter the status column to use the enum type
ALTER TABLE "order"
ALTER COLUMN status TYPE order_status USING status::order_status;

-- Add coffee_shop_id column to the customer table
ALTER TABLE "customer"
ADD COLUMN coffee_shop_id INT,
ADD FOREIGN KEY (coffee_shop_id) REFERENCES coffee_shop(id) ON DELETE RESTRICT;

-- drop the unique constraint from the customer phone no only
ALTER TABLE customer
DROP CONSTRAINT customer_phone_no_key;

-- add unique constraint on a combination of phone_no with shop_id
ALTER TABLE customer
ADD CONSTRAINT unique_phone_shop
UNIQUE (phone_no, coffee_shop_id);




