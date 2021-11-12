-- migrate:up
CREATE OR REPLACE FUNCTION update_last_modified_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_modified_at = now();
    RETURN NEW;   
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cart_modtime BEFORE UPDATE ON cart FOR EACH ROW EXECUTE PROCEDURE update_last_modified_at_column();

-- migrate:down
DROP FUNCTION update_last_modified_at_column;
DROP TRIGGER update_cart_modtime;
