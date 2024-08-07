-- User roles enum
CREATE TYPE user_role AS ENUM ('CASHIER', 'CHEF', 'ORDER_RECEIVER', 'ADMIN');

-- coffee_shop table
CREATE TABLE coffee_shop (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255)
);

-- branches table
CREATE TABLE branch (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    deleted BOOLEAN DEFAULT FALSE,
    coffee_shop_id INT,
    FOREIGN KEY (coffee_shop_id) REFERENCES coffee_shop(id) ON DELETE RESTRICT
);

-- users table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone_no VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role user_role NOT NULL,
    password VARCHAR(255) NOT NULL,
    deleted BOOLEAN DEFAULT FALSE,
    branch_id INT,
    FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE RESTRICT
);

-- relationship table (branches - users)
CREATE TABLE branch_user (
    branch_id INT NOT NULL,
    manager_id INT NOT NULL,
    PRIMARY KEY (branch_id, manager_id),
    FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE RESTRICT,
    FOREIGN KEY (manager_id) REFERENCES "user"(id) ON DELETE RESTRICT
);

-- inventory_items table
CREATE TABLE inventory_item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    expire_date DATE,
    prod_date DATE,
    available_quantity INT NOT NULL,
    deleted BOOLEAN DEFAULT FALSE,
    inventory_manager_id INT,
    FOREIGN KEY (inventory_manager_id) REFERENCES "user"(id) ON DELETE RESTRICT
);

-- menu_items table
CREATE TABLE menu_item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    price DOUBLE PRECISION NOT NULL,
    deleted BOOLEAN DEFAULT FALSE
);

-- customers table
CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    deleted BOOLEAN DEFAULT FALSE,
    phone_no VARCHAR(20) NOT NULL UNIQUE
);

-- orders table
CREATE TABLE "order" (
    id SERIAL PRIMARY KEY,
    issue_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    customer_id INT,
    employee_id INT,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE RESTRICT,
    FOREIGN KEY (employee_id) REFERENCES "user"(id) ON DELETE RESTRICT
);

-- order_items table
CREATE TABLE order_item (
    order_id INT,
    item_id INT,
    quantity INT NOT NULL,
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES "order"(id) ON DELETE RESTRICT,
    FOREIGN KEY (item_id) REFERENCES menu_item(id) ON DELETE RESTRICT
);

