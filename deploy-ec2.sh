#!/bin/bash
# DataDoctor AI — EC2 Quick Setup Script
# Run this ON the EC2 instance after SSH-ing in
# Usage: bash deploy-ec2.sh

set -e

echo "🩺 DataDoctor AI — EC2 Deployment"
echo "=================================="

# Update system
echo "📦 Updating system packages..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git

# Clone the repo
echo "📥 Cloning repository..."
cd /home/ubuntu
if [ -d "datadoctor" ]; then
    cd datadoctor
    git pull origin main
else
    git clone https://github.com/i-fren/ai-csv-cleaner.git datadoctor
    cd datadoctor
fi

# Setup Python virtual environment
echo "🐍 Setting up Python environment..."
cd /home/ubuntu/datadoctor/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Setup systemd service
echo "⚙️ Configuring systemd service..."
sudo cp /home/ubuntu/datadoctor/backend/datadoctor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable datadoctor
sudo systemctl restart datadoctor

# Wait and check
sleep 3
echo ""
echo "✅ Deployment complete!"
echo ""
echo "Checking health..."
curl -s http://localhost:8000/health
echo ""
echo ""
echo "=================================="
echo "🌐 Your API is live at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
echo "📖 API Docs: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000/docs"
echo ""
echo "To set your OpenAI key (optional):"
echo "  sudo nano /etc/systemd/system/datadoctor.service"
echo "  # Change OPENAI_API_KEY line"
echo "  sudo systemctl daemon-reload && sudo systemctl restart datadoctor"
