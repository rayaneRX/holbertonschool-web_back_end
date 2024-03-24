-- script that creates a trigger that decreases the quantity
DROP TRIGGER IF EXISTS decrease_stock;
CREATE TRIGGER decrease_stock AFTER INSERT ON orders
FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;