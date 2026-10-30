-- FoundIt Lost and Found System: database setup
CREATE DATABASE IF NOT EXISTS foundit_db;
USE foundit_db;

CREATE TABLE IF NOT EXISTS items (
    item_id       INT AUTO_INCREMENT PRIMARY KEY,
    item_name     VARCHAR(100) NOT NULL,
    description   TEXT,
    item_type     ENUM('Lost', 'Found') NOT NULL,
    location      VARCHAR(150) NOT NULL,
    date_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status        ENUM('Pending', 'Claimed', 'Returned') NOT NULL DEFAULT 'Pending'
);

-- Sample data (optional)
INSERT INTO items (item_name, description, item_type, location) VALUES
('Black Umbrella', 'Foldable, with a wooden handle', 'Found', 'Library'),
('Blue Wallet', 'Contains student ID', 'Lost', 'Canteen'),
('Water Bottle', 'Green tumbler with stickers', 'Found', 'Gymnasium');

-- Check the data
SELECT * FROM items;
