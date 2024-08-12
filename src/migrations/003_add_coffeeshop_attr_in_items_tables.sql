-- Remove the inventory_manager_id column from the inventory_item table
ALTER TABLE inventory_item
DROP COLUMN inventory_manager_id;

-- Add the coffee_shop_id column to the inventory_item table
ALTER TABLE inventory_item
ADD COLUMN coffee_shop_id INT,
ADD CONSTRAINT fk_inventory_item_coffee_shop
FOREIGN KEY (coffee_shop_id) REFERENCES coffee_shop(id) ON DELETE RESTRICT;

-- Add the coffee_shop_id column to the menu_item table
ALTER TABLE menu_item
ADD COLUMN coffee_shop_id INT,
ADD CONSTRAINT fk_menu_item_coffee_shop
FOREIGN KEY (coffee_shop_id) REFERENCES coffee_shop(id) ON DELETE RESTRICT;
