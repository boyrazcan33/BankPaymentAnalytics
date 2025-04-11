import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def ensure_datetime(dt):
    """Ensure a value is a datetime object"""
    if isinstance(dt, str):
        return pd.to_datetime(dt).to_pydatetime()
    elif isinstance(dt, pd.Timestamp):
        return dt.to_pydatetime()
    elif isinstance(dt, pd.Series):
        return dt.iloc[0].to_pydatetime()
    elif isinstance(dt, np.datetime64):
        return pd.Timestamp(dt).to_pydatetime()
    return dt

def random_date(start, end):
    """Generate a random date between start and end"""
    if not isinstance(start, datetime):
        start = ensure_datetime(start)
    if not isinstance(end, datetime):
        end = ensure_datetime(end)
    
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)