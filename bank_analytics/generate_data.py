import numpy as np
import random
import pandas as pd
from datetime import datetime
from psycopg2.extras import execute_values

# Import custom modules
from db.connection import get_connection
from data_generators.customers import generate_customers
from data_generators.products import generate_products
from data_generators.contracts import generate_contracts
from data_generators.payments import generate_payments
from data_generators.customer_service import generate_customer_service
from schema.create_tables import create_tables

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

# Define data generation parameters
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 10
NUM_CONTRACTS = 1000
NUM_PAYMENTS = 5000
NUM_CUSTOMER_SERVICE = 800

# Date ranges
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 4, 1)
CURRENT_DATE = datetime(2024, 4, 1)

# Insert data into tables
def insert_data(conn, customers_df, products_df, contracts_df, payments_df, cs_df):
    """Insert generated data into database tables"""
    with conn.cursor() as cur:
        print("Inserting customers...")
        execute_values(cur, 
            "INSERT INTO customers (customer_id, name, email, phone, signup_date, risk_score, acquisition_channel, acquisition_cost) VALUES %s",
            [tuple(x) for x in customers_df.values])
        
        print("Inserting products...")
        execute_values(cur, 
            "INSERT INTO products (product_id, name, category, launch_date, min_risk_score, interest_rate_min, interest_rate_max) VALUES %s",
            [tuple(x) for x in products_df.values])
        
        print("Inserting contracts...")
        execute_values(cur, 
            "INSERT INTO contracts (contract_id, customer_id, product_id, contract_type, start_date, end_date, amount, interest_rate, status, renewal_contract_id) VALUES %s",
            [tuple(x) for x in contracts_df.values])
        
        print("Inserting payments...")
        # Fix NaT values in the payments_df - replace with None (SQL NULL)
        payment_values = []
        for row in payments_df.itertuples(index=False):
            row_list = list(row)
            # Convert any pd.NaT values to None
            for i, val in enumerate(row_list):
                if pd.isna(val):
                    row_list[i] = None
            payment_values.append(tuple(row_list))
        
        execute_values(cur, 
            "INSERT INTO payments (payment_id, contract_id, scheduled_amount, principal_amount, interest_amount, fee_amount, paid_amount, due_date, payment_at, status) VALUES %s",
            payment_values)
        
        print("Inserting customer service tickets...")
        # Also fix potential NaT values in customer_service df
        cs_values = []
        for row in cs_df.itertuples(index=False):
            row_list = list(row)
            # Convert any pd.NaT values to None
            for i, val in enumerate(row_list):
                if pd.isna(val):
                    row_list[i] = None
            cs_values.append(tuple(row_list))
            
        execute_values(cur, 
            "INSERT INTO customer_service (ticket_id, customer_id, contract_id, created_at, resolved_at, issue_type, satisfaction_score) VALUES %s",
            cs_values)
        
        conn.commit()

# Main function
def main():
    try:
        # Generate data
        print("Generating customers data...")
        customers_df = generate_customers(NUM_CUSTOMERS, START_DATE, END_DATE)
        
        print("Generating products data...")
        products_df = generate_products(NUM_PRODUCTS, START_DATE)
        
        print("Generating contracts data...")
        contracts_df = generate_contracts(customers_df, products_df, END_DATE, CURRENT_DATE)
        
        print("Generating payments data...")
        payments_df = generate_payments(contracts_df, CURRENT_DATE, NUM_PAYMENTS)
        
        print("Generating customer service data...")
        cs_df = generate_customer_service(customers_df, contracts_df, payments_df, NUM_CUSTOMER_SERVICE, START_DATE, CURRENT_DATE)
        
        # Connect to database
        print("Connecting to PostgreSQL database...")
        conn = get_connection()
        
        # Create tables
        print("Creating database tables...")
        create_tables(conn)
        
        # Insert data
        print("Inserting data into tables...")
        insert_data(conn, customers_df, products_df, contracts_df, payments_df, cs_df)
        
        print(f"Data generation complete!")
        print(f"Generated {len(customers_df)} customers")
        print(f"Generated {len(products_df)} products")
        print(f"Generated {len(contracts_df)} contracts")
        print(f"Generated {len(payments_df)} payments")
        print(f"Generated {len(cs_df)} customer service tickets")
        
        # Close connection
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()