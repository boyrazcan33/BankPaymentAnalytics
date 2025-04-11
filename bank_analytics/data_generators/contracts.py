import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from utils.date_utils import random_date, ensure_datetime

def generate_contracts(customers, products, end_date, current_date):
    """Generate contract data"""
    contracts = []
    
    # Each customer should have 1-4 contracts
    for customer_id in customers['customer_id'].values:
        num_contracts = random.choices([1, 2, 3, 4], weights=[0.4, 0.3, 0.2, 0.1])[0]
        
        # Get signup date from customer
        customer_row = customers[customers['customer_id'] == customer_id]
        signup_date = datetime.strptime(str(customer_row['signup_date'].values[0])[:10], '%Y-%m-%d')
        
        for _ in range(num_contracts):
            product = products.iloc[random.randint(0, len(products) - 1)]
            
            # Ensure end_date is datetime
            if not isinstance(end_date, datetime):
                end_date = datetime.strptime(str(end_date)[:10], '%Y-%m-%d')
            
            start_date_contract = random_date(signup_date, end_date)
            
            # Contract duration based on type
            if product['category'] == 'BNPL':
                duration_months = random.choice([1, 2, 3, 6])
            elif product['category'] == 'Hire Purchase':
                duration_months = random.choice([12, 24, 36, 48, 60])
            elif product['category'] == 'Mortgage':
                duration_months = random.choice([180, 240, 300, 360])
            else:  # Consumer Loan, Credit Line
                duration_months = random.choice([6, 12, 18, 24, 36])
            
            end_date_contract = start_date_contract + timedelta(days=30 * duration_months)
            
            # Determine status based on dates
            if end_date_contract > current_date:
                status = random.choices(['active', 'cancelled'], weights=[0.95, 0.05])[0]
            else:
                status = random.choices(['completed', 'default'], weights=[0.95, 0.05])[0]
            
            # Create contract
            contract_id = len(contracts) + 1
            
            # Set interest rate based on product min/max and customer risk score
            customer_risk = float(customer_row['risk_score'].values[0])
            risk_range = 850 - 550  # Max risk score - min risk score
            rate_position = (customer_risk - 550) / risk_range  # Normalized position in risk range
            
            interest_rate = float(product['interest_rate_min']) + (float(product['interest_rate_max']) - float(product['interest_rate_min'])) * (1 - rate_position)
            interest_rate = round(max(float(product['interest_rate_min']), min(float(product['interest_rate_max']), interest_rate)), 2)
            
            # Set amount based on product type
            if product['category'] == 'BNPL':
                amount = round(random.uniform(100, 2000), 2)
            elif product['category'] == 'Hire Purchase':
                amount = round(random.uniform(5000, 50000), 2)
            elif product['category'] == 'Mortgage':
                amount = round(random.uniform(100000, 500000), 2)
            elif product['category'] == 'Consumer Loan':
                amount = round(random.uniform(1000, 25000), 2)
            else:  # Credit Line
                amount = round(random.uniform(2000, 20000), 2)
            
            contracts.append({
                'contract_id': contract_id,
                'customer_id': customer_id,
                'product_id': product['product_id'],
                'contract_type': product['category'],
                'start_date': start_date_contract,
                'end_date': end_date_contract,
                'amount': amount,
                'interest_rate': interest_rate,
                'status': status,
                'renewal_contract_id': None  # Will update some of these later
            })
    
    contracts_df = pd.DataFrame(contracts)
    
    # Add some renewal relationships (10% of completed contracts get renewed)
    completed_contracts = contracts_df[contracts_df['status'] == 'completed']
    
    for _, old_contract in completed_contracts.sample(frac=0.1).iterrows():
        # Get the end date from the old contract
        old_end_date = old_contract['end_date']
        
        # Find a newer contract for the same customer with same product type
        newer_contracts = contracts_df[
            (contracts_df['customer_id'] == old_contract['customer_id']) &
            (contracts_df['contract_type'] == old_contract['contract_type'])
        ]
        
        if not newer_contracts.empty:
            for idx, newer_contract in newer_contracts.iterrows():
                if newer_contract['start_date'] > old_end_date:
                    # Update the renewal_contract_id
                    contracts_df.loc[contracts_df['contract_id'] == old_contract['contract_id'], 'renewal_contract_id'] = newer_contract['contract_id']
                    break
    
    return contracts_df