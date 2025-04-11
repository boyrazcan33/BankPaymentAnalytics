def create_tables(conn):
    """Create database tables"""
    with conn.cursor() as cur:
        # Drop tables if they exist
        cur.execute("DROP TABLE IF EXISTS customer_service, payments, contracts, products, customers CASCADE;")
        
        # Create tables
        cur.execute("""
        CREATE TABLE customers (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(50),
            signup_date DATE,
            risk_score DECIMAL(5,2),
            acquisition_channel VARCHAR(50),
            acquisition_cost DECIMAL(10,2)
        );
        """)
        
        cur.execute("""
        CREATE TABLE products (
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            category VARCHAR(50),
            launch_date DATE,
            min_risk_score DECIMAL(5,2),
            interest_rate_min DECIMAL(5,2),
            interest_rate_max DECIMAL(5,2)
        );
        """)
        
        cur.execute("""
        CREATE TABLE contracts (
            contract_id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            product_id INTEGER REFERENCES products(product_id),
            contract_type VARCHAR(50),
            start_date DATE,
            end_date DATE,
            amount DECIMAL(12,2),
            interest_rate DECIMAL(5,2),
            status VARCHAR(20),
            renewal_contract_id INTEGER NULL
        );
        """)
        
        # Add foreign key constraint after table is created
        cur.execute("""
        ALTER TABLE contracts 
        ADD CONSTRAINT fk_renewal_contract 
        FOREIGN KEY (renewal_contract_id) 
        REFERENCES contracts(contract_id);
        """)
        
        cur.execute("""
        CREATE TABLE payments (
            payment_id SERIAL PRIMARY KEY,
            contract_id INTEGER REFERENCES contracts(contract_id),
            scheduled_amount DECIMAL(12,2),
            principal_amount DECIMAL(12,2),
            interest_amount DECIMAL(12,2),
            fee_amount DECIMAL(12,2),
            paid_amount DECIMAL(12,2),
            due_date DATE,
            payment_at DATE,
            status VARCHAR(20)
        );
        """)
        
        cur.execute("""
        CREATE TABLE customer_service (
            ticket_id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            contract_id INTEGER REFERENCES contracts(contract_id),
            created_at TIMESTAMP,
            resolved_at TIMESTAMP,
            issue_type VARCHAR(50),
            satisfaction_score INTEGER
        );
        """)
        
        conn.commit()