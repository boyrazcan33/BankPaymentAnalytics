import pandas as pd
import random
from datetime import timedelta
from utils.date_utils import random_date

def generate_products(num_products, start_date):
    """Generate product data"""
    products = []
    categories = ['Consumer Loan', 'BNPL', 'Hire Purchase', 'Credit Line', 'Mortgage']
    
    product_names = {
        'Consumer Loan': ['Personal Loan', 'Quick Cash', 'Signature Loan', 'Debt Consolidation Loan'],
        'BNPL': ['FlexiPay', 'PayLater', 'EasyBuy', 'SplitPay'],
        'Hire Purchase': ['Auto Finance', 'Equipment Lease', 'Asset Finance', 'Machinery Purchase'],
        'Credit Line': ['FlexiCredit', 'CreditPlus', 'RevolvingCredit', 'CashLine'],
        'Mortgage': ['HomeLoan', 'PropertyFinance', 'RealEstateLoan', 'MortgagePlus']
    }
    
    for i in range(1, num_products + 1):
        category = random.choice(categories)
        products.append({
            'product_id': i,
            'name': random.choice(product_names[category]),
            'category': category,
            'launch_date': random_date(start_date - timedelta(days=365), start_date + timedelta(days=180)),
            'min_risk_score': round(random.uniform(580, 700), 2),
            'interest_rate_min': round(random.uniform(0, 8), 2) if category != 'BNPL' else 0,
            'interest_rate_max': round(random.uniform(8, 18), 2) if category != 'BNPL' else 0
        })
    
    return pd.DataFrame(products)