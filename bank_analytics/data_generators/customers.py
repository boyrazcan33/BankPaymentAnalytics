import pandas as pd
import random
from faker import Faker
from utils.date_utils import random_date

# Set up Faker
fake = Faker()

def generate_customers(num_customers, start_date, end_date):
    """Generate customer data"""
    customers = []
    acquisition_channels = ['Direct', 'Referral', 'Paid Search', 'Affiliate', 'Social Media', 'Email Campaign']
    
    for i in range(1, num_customers + 1):
        signup_date = random_date(start_date, end_date)
        
        # Create a shorter, more consistent phone format
        phone = f"+{random.randint(1, 99)}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        
        customers.append({
            'customer_id': i,
            'name': fake.name(),
            'email': fake.email(),
            'phone': phone,  # Controlled phone format
            'signup_date': signup_date,
            'risk_score': round(random.uniform(550, 850), 2),
            'acquisition_channel': random.choice(acquisition_channels),
            'acquisition_cost': round(random.uniform(10, 80), 2)
        })
    
    return pd.DataFrame(customers)