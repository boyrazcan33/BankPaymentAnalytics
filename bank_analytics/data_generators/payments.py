import pandas as pd
import random
from datetime import timedelta
from utils.date_utils import ensure_datetime

def generate_payments(contracts, current_date, num_payments_limit=None):
    """Generate payment data"""
    payments = []
    payment_id = 1
    
    for _, contract in contracts.iterrows():
        # Skip generating payments for cancelled contracts
        if contract['status'] == 'cancelled':
            continue
            
        # Determine payment frequency (monthly for most products)
        if contract['contract_type'] == 'BNPL':
            # Bi-weekly for BNPL
            payment_interval = timedelta(days=14)
        else:
            # Monthly for others
            payment_interval = timedelta(days=30)
        
        # Convert contract dates to datetime objects
        start_date_contract = ensure_datetime(contract['start_date'])
        end_date_contract = ensure_datetime(contract['end_date'])
        
        # Calculate number of payments and payment amount
        contract_duration = end_date_contract - start_date_contract
        num_payments_total = max(1, int(contract_duration.days / payment_interval.days))
        
        base_payment_amount = contract['amount'] / num_payments_total
        
        # Handle different scenarios for payments
        for i in range(num_payments_total):
            # Due date is calculated from start date
            due_date = start_date_contract + payment_interval * (i + 1)
            
            # Skip future payments for active contracts (only create scheduled ones)
            if due_date > current_date:
                # Create scheduled future payment
                status = 'scheduled'
                payment_at = None  # This will become NULL in the database, not NaT
            else:
                # Create historical payment with appropriate status
                on_time_probability = 0.85 if contract['status'] != 'default' else 0.5
                
                if random.random() < on_time_probability:
                    # On-time payment
                    status = 'completed'
                    # Payment made 0-3 days before due date
                    payment_at = due_date - timedelta(days=random.randint(0, 3))
                else:
                    # Late payment options
                    late_options = ['late', 'partial', 'missed']
                    late_weights = [0.7, 0.2, 0.1]
                    status = random.choices(late_options, weights=late_weights)[0]
                    
                    if status == 'late':
                        # Payment made 1-10 days after due date
                        payment_at = due_date + timedelta(days=random.randint(1, 10))
                    elif status == 'partial':
                        # Partial payment made around due date (-2 to +5 days)
                        payment_at = due_date + timedelta(days=random.randint(-2, 5))
                    else:  # missed
                        payment_at = None  # This will become NULL in the database, not NaT
            
            # Calculate payment amounts
            scheduled_amount = round(base_payment_amount, 2)
            
            # Calculate principal and interest components
            if contract['interest_rate'] > 0:
                # Simple interest calculation for demo purposes
                remaining_principal = contract['amount'] - (base_payment_amount * i)
                monthly_interest_rate = contract['interest_rate'] / 12 / 100
                interest_amount = round(remaining_principal * monthly_interest_rate, 2)
                principal_amount = round(scheduled_amount - interest_amount, 2)
            else:
                # No interest (e.g., BNPL)
                interest_amount = 0
                principal_amount = scheduled_amount
            
            # Add occasional fees
            fee_amount = 0
            if status == 'late' and random.random() < 0.7:
                fee_amount = round(random.uniform(15, 35), 2)
            elif status == 'missed' and random.random() < 0.8:
                fee_amount = round(random.uniform(25, 50), 2)
            
            # Determine paid amount based on status
            if status == 'completed':
                paid_amount = scheduled_amount
            elif status == 'partial':
                paid_amount = round(scheduled_amount * random.uniform(0.4, 0.8), 2)
            elif status == 'late':
                paid_amount = scheduled_amount + fee_amount
            else:  # missed or scheduled
                paid_amount = 0
                
            payments.append({
                'payment_id': payment_id,
                'contract_id': contract['contract_id'],
                'scheduled_amount': scheduled_amount,
                'principal_amount': principal_amount,
                'interest_amount': interest_amount,
                'fee_amount': fee_amount,
                'paid_amount': paid_amount,
                'due_date': due_date,
                'payment_at': payment_at,
                'status': status
            })
            
            payment_id += 1
    
    # Create DataFrame from payments list
    payments_df = pd.DataFrame(payments)
    
    # Limit to desired number if provided
    if num_payments_limit and len(payments_df) > num_payments_limit:
        payments_df = payments_df.sample(num_payments_limit).reset_index(drop=True)
    
    return payments_df