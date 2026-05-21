#!/bin/bash
# DataDoctor AI - Backend startup script for EC2

set -e

echo "=== DataDoctor AI Backend Setup ==="

# Update system
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git

# Create app directory
mkdir -p /home/ubuntu/datadoctor
cd /home/ubuntu/datadoctor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install fastapi==0.111.0 "uvicorn[standard]==0.29.0" pandas==2.2.2 \
    scikit-learn==1.4.2 openai==1.30.1 reportlab==4.2.0 \
    python-multipart==0.0.9 numpy==1.26.4

echo "=== Dependencies installed ==="

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
