-- Create tables for egg production database

-- Provinces table
CREATE TABLE provinces (
    id SERIAL PRIMARY KEY,
    province_name VARCHAR(255) NOT NULL
);

-- Districts table with foreign key to provinces
CREATE TABLE districts (
    id SERIAL PRIMARY KEY,
    province_id INTEGER REFERENCES provinces(id) ON DELETE CASCADE,
    district_name VARCHAR(255) NOT NULL
);

-- Households table with foreign keys to provinces and districts
CREATE TABLE households (
    id SERIAL PRIMARY KEY,
    province_id INTEGER REFERENCES provinces(id) ON DELETE CASCADE,
    district_id INTEGER REFERENCES districts(id) ON DELETE CASCADE,
    clust INTEGER NOT NULL,
    owner VARCHAR(255) NOT NULL,
    household_weight FLOAT8 NOT NULL,
    yield BOOLEAN NOT NULL,
    produced_eggs_last_six_months BOOLEAN NOT NULL
);

-- Eggs production table with foreign key to households
CREATE TABLE eggs_production (
    id SERIAL PRIMARY KEY,
    household_id INTEGER REFERENCES households(id) ON DELETE CASCADE,
    month VARCHAR(255) NOT NULL,
    laying_hens INTEGER NOT NULL,
    eggs_produced INTEGER NOT NULL,
    eggs_consumed INTEGER NOT NULL,
    eggs_sold INTEGER NOT NULL,
    egg_unit_price INTEGER NOT NULL,
    hatched_eggs INTEGER NOT NULL,
    eggs_for_other_usages INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create audit log table for tracking changes
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100)
);

-- Create a stored procedure for data validation
CREATE OR REPLACE PROCEDURE validate_eggs_production_data(
    p_household_id INTEGER,
    p_month VARCHAR(255),
    p_laying_hens INTEGER,
    p_eggs_produced INTEGER,
    p_eggs_consumed INTEGER,
    p_eggs_sold INTEGER,
    p_hatched_eggs INTEGER,
    p_eggs_other INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    total_eggs INTEGER;
BEGIN
    -- Calculate total eggs distributed
    total_eggs := p_eggs_consumed + p_eggs_sold + p_hatched_eggs + p_eggs_other;
    
    -- Validate laying hens
    IF p_laying_hens < 0 THEN
        RAISE EXCEPTION 'Number of laying hens cannot be negative';
    END IF;
    
    -- Validate eggs produced and distributed match
    IF p_eggs_produced < total_eggs THEN
        RAISE EXCEPTION 'Sum of distributed eggs cannot exceed total eggs produced';
    END IF;
    
    -- If all validations pass, insert the data
    INSERT INTO eggs_production (
        household_id, month, laying_hens, eggs_produced,
        eggs_consumed, eggs_sold, egg_unit_price,
        hatched_eggs, eggs_for_other_usages
    ) VALUES (
        p_household_id, p_month, p_laying_hens, p_eggs_produced,
        p_eggs_consumed, p_eggs_sold, 0, -- default price
        p_hatched_eggs, p_eggs_other
    );
END;
$$;

-- Create trigger for logging changes
CREATE OR REPLACE FUNCTION log_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, changed_by)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', current_user);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, changed_by)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', current_user);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, action, changed_by)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', current_user);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all tables
CREATE TRIGGER provinces_audit
AFTER INSERT OR UPDATE OR DELETE ON provinces
FOR EACH ROW EXECUTE FUNCTION log_changes();

CREATE TRIGGER districts_audit
AFTER INSERT OR UPDATE OR DELETE ON districts
FOR EACH ROW EXECUTE FUNCTION log_changes();

CREATE TRIGGER households_audit
AFTER INSERT OR UPDATE OR DELETE ON households
FOR EACH ROW EXECUTE FUNCTION log_changes();

CREATE TRIGGER eggs_production_audit
AFTER INSERT OR UPDATE OR DELETE ON eggs_production
FOR EACH ROW EXECUTE FUNCTION log_changes();