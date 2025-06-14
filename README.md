# FinOps Dashboard for AWS Free Tier Monitoring

![FinOps Architecture Diagram](architecture.png)

A monitoring solution that tracks AWS Free Tier usage and provides cost visibility to prevent unexpected charges.

## Features

- **Daily AWS Cost Collection**: Automatically fetches cost and usage data from AWS Cost Explorer API
- **SQLite Database**: Lightweight storage for historical usage data
- **Grafana Dashboard**: Visualize usage trends and cost metrics
- **Alerting System**: Get notified when approaching Free Tier limits
- **Cron Automation**: Scheduled daily data collection

## Architecture

```mermaid
graph TD
    A[AWS Services] -->|API Calls| B[EC2 Ubuntu Instance]
    B --> C[Python Data Collector]
    C --> D[SQLite Database]
    D --> E[Grafana Dashboard]
    E --> F[Alerts]
