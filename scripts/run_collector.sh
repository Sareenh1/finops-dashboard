#!/bin/bash
cd /home/ubuntu/finops-dashboard
source venv/bin/activate
python3 scripts/aws_cost_collector.py >> logs/cost_collector.log 2>&1
