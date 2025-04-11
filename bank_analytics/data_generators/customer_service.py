import pandas as pd
import random
from datetime import timedelta
from utils.date_utils import random_date

def generate_customer_service(customers, contracts, payments, num_tickets, start_date, current_date):
    """Generate customer service data"""
    tickets = []
    issue_types = [
        'payment not showing', 'payment failed', 'incorrect payment amount', 
        'late fee dispute', 'autopay setup issue', 'login problem',
        'account access', 'statement question', 'interest rate inquiry',
        'contract terms', 'early payoff request', 'payment method update'
    ]
    
    # Generate tickets, some related to payments, some not
    for i in range(1, num_tickets + 1):
        # Randomly select a customer
        customer_id = random.choice(customers['customer_id'].tolist())
        
        # Get their contracts - use .tolist() to avoid pandas indexing issues
        customer_contracts = contracts[contracts['customer_id'] == customer_id]
        
        if customer_contracts.empty:
            continue
            
        # Use .iloc to select a random row, then get the contract_id from that row
        random_idx = random.randint(0, len(customer_contracts) - 1)
        contract_id = customer_contracts.iloc[random_idx]['contract_id']
        
        # 70% of tickets should be related to payments
        if random.random() < 0.7:
            # Find a payment for this contract
            contract_payments = payments[payments['contract_id'] == contract_id]
            
            if not contract_payments.empty:
                # Pick a payment, preferring problematic ones
                problem_payments = contract_payments[contract_payments['status'].isin(['late', 'partial', 'missed'])]
                
                if not problem_payments.empty:
                    payment_idx = random.randint(0, len(problem_payments) - 1)
                    payment = problem_payments.iloc[payment_idx]
                else:
                    payment_idx = random.randint(0, len(contract_payments) - 1)
                    payment = contract_payments.iloc[payment_idx]
                
                # Create ticket near payment date
                if pd.notna(payment['payment_at']):
                    created_at = payment['payment_at'] + timedelta(days=random.randint(0, 5))
                else:
                    created_at = payment['due_date'] + timedelta(days=random.randint(1, 10))
                
                # Cap at current date
                created_at = min(created_at, current_date)
                
                # Payment-related issue type
                issue_type = random.choice(issue_types[:5])  # First 5 are payment-related
            else:
                created_at = random_date(start_date, current_date)
                issue_type = random.choice(issue_types)
        else:
            created_at = random_date(start_date, current_date)
            issue_type = random.choice(issue_types[5:])  # Non-payment issues
        
        # Resolved tickets (90% get resolved)
        if random.random() < 0.9:
            # Resolution takes 1 hour to 5 days
            resolution_time = timedelta(hours=random.randint(1, 120))
            resolved_at = created_at + resolution_time
            
            # Cap at current date
            resolved_at = min(resolved_at, current_date)
        else:
            resolved_at = None
        
        # Satisfaction score for resolved tickets (1-5 scale)
        if resolved_at is not None:
            # Distribution favoring 4-5 scores
            satisfaction_score = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.15, 0.3, 0.4])[0]
        else:
            satisfaction_score = None
        
        tickets.append({
            'ticket_id': i,
            'customer_id': customer_id,
            'contract_id': contract_id,
            'created_at': created_at,
            'resolved_at': resolved_at,
            'issue_type': issue_type,
            'satisfaction_score': satisfaction_score
        })
    
    return pd.DataFrame(tickets)