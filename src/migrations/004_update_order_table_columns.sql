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