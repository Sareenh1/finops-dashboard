# FinOps Dashboard for AWS Free Tier Monitoring

This project monitors AWS Free Tier usage and provides visibility into potential cost overruns.

## Features
- Daily collection of AWS cost and usage data
- SQLite database for storage
- Grafana dashboard for visualization
- Alerting for free tier limit breaches

## Setup
1. Install requirements: `sudo apt install python3 python3-pip awscli sqlite3 grafana`
2. Configure AWS CLI: `aws configure`
3. Set up cron job for daily data collection
4. Configure Grafana with SQLite data source
