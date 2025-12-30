-- 1. Companies
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- 2. Warehouses
CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    location_address TEXT
);

-- 3. Suppliers
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255)
);

-- 4. Products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    supplier_id INTEGER REFERENCES suppliers(id),
    sku VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2),
    low_stock_threshold INTEGER DEFAULT 10,
    UNIQUE(company_id, sku)
);

-- 5. Inventory (The Link)
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    warehouse_id INTEGER REFERENCES warehouses(id),
    quantity INTEGER DEFAULT 0,
    UNIQUE(product_id, warehouse_id)
);

-- 6. Product Bundles
CREATE TABLE product_bundles (
    parent_product_id INTEGER REFERENCES products(id),
    child_product_id INTEGER REFERENCES products(id),
    quantity_needed INTEGER NOT NULL
);