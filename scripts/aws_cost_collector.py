import boto3
import sqlite3
from datetime import datetime, timedelta
import pytz
import pandas as pd

# Initialize clients
ce = boto3.client('ce')
ec2 = boto3.client('ec2')

# Database setup
conn = sqlite3.connect('/var/lib/grafana/aws_data/aws_usage.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS aws_usage (
    date TEXT PRIMARY KEY,
    estimated_cost REAL,
    ec2_running_hours REAL,
    s3_storage_gb REAL,
    rds_running_hours REAL,
    lambda_invocations INTEGER,
    data_transfer_gb REAL
)
''')

def get_cost_and_usage():
    # Get dates for the last day
    end_date = datetime.now(pytz.utc)
    start_date = end_date - timedelta(days=1)
    
    # Format dates for AWS API
    start = start_date.strftime('%Y-%m-%d')
    end = end_date.strftime('%Y-%m-%d')
    
    # Get cost data
    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )
    
    # Process cost data
    cost_data = {}
    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])
        cost_data[service] = amount
    
    # Get EC2 running hours (simplified)
    ec2_response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    ec2_hours = len(ec2_response['Reservations']) * 24  # Simplified calculation
    
    # Prepare data for DB
    data = {
        'date': start,
        'estimated_cost': sum(cost_data.values()),
        'ec2_running_hours': ec2_hours,
        's3_storage_gb': 0,  # Placeholder - add S3 logic
        'rds_running_hours': 0,  # Placeholder - add RDS logic
        'lambda_invocations': cost_data.get('Lambda', 0) * 1000,  # Simplified
        'data_transfer_gb': cost_data.get('AWS Data Transfer', 0) * 100  # Simplified
    }
    
    # Insert into DB
    cursor.execute('''
    INSERT OR REPLACE INTO aws_usage 
    (date, estimated_cost, ec2_running_hours, s3_storage_gb, rds_running_hours, lambda_invocations, data_transfer_gb)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', tuple(data.values()))
    
    conn.commit()
    return data

if __name__ == "__main__":
    data = get_cost_and_usage()
    print(f"Data collected for {data['date']}:")
    print(pd.DataFrame([data]))
