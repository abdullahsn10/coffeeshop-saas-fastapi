-- add created column to customer table
ALTER TABLE customer
ADD COLUMN created TIMESTAMP DEFAULT CURRENT_TIMESTAMP;