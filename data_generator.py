import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# 1. Generate CRM Data (Revenue)
customers = [f"Company {i}" for i in range(1, 101)]
tiers = ['Enterprise', 'Mid-Market', 'SMB']
crm_data = pd.DataFrame({
    'customer_name': customers,
    'tier': [random.choice(tiers) for _ in range(100)],
    'mrr': [random.randint(500, 15000) for _ in range(100)],
    'contract_start': [(datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d') for _ in range(100)]
})

# 2. Generate Support Data (Friction)
support_data = pd.DataFrame({
    'ticket_id': [f"TKT-{i}" for i in range(1000, 1200)],
    'customer_name': [random.choice(customers) for _ in range(200)],
    'sentiment_score': [round(random.uniform(1, 5), 1) for _ in range(200)], # 1 is angry, 5 is happy
    'complexity_score': [random.randint(1, 10) for _ in range(200)]
})

# 3. Generate Product Usage (Engagement)
usage_data = pd.DataFrame({
    'customer_name': customers,
    'last_login_days_ago': [random.randint(0, 45) for _ in range(100)],
    'feature_adoption_rate': [round(random.uniform(0.1, 0.9), 2) for _ in range(100)]
})

# Save to CSV
crm_data.to_csv('crm_data.csv', index=False)
support_data.to_csv('support_data.csv', index=False)
usage_data.to_csv('usage_data.csv', index=False)

print("✅ Revenue Bridge datasets generated: crm_data.csv, support_data.csv, usage_data.csv")
