import random
import pandas as pd
import string
from datetime import timedelta

def generate_data(num_rows, data_config):
    """Generates synthetic data based on user configurations"""
    new_data = []
    
    for _ in range(num_rows):
        row = {}
        for col, (dtype, *args) in data_config.items():
            if dtype == "Same Value":
                row[col] = args[0]
            elif dtype == "Random":
                row[col] = "".join(random.choices(string.ascii_letters, k=8))
            elif dtype == "Number Range":
                row[col] = random.randint(args[0], args[1])
            elif dtype == "Date":
                start_date, end_date = args
                delta = end_date - start_date
                row[col] = start_date + timedelta(days=random.randint(0, delta.days))
            elif dtype == "Text":
                row[col] = "".join(random.choices(string.ascii_letters, k=args[0]))
        new_data.append(row)
    
    return pd.DataFrame(new_data)
