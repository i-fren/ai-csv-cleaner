#!/bin/bash
# DataDoctor AI - Full deployment script
# Usage: ./deploy.sh <EC2_PUBLIC_IP> <S3_BUCKET_NAME> <PEM_KEY_PATH>
# Example: ./deploy.sh 54.123.45.67 datadoctor-frontend ~/.ssh/my-key.pem

EC2_IP=$1
S3_BUCKET=$2
PEM_KEY=$3

if [ -z "$EC2_IP" ] || [ -z "$S3_BUCKET" ] || [ -z "$PEM_KEY" ]; then
  echo "Usage: ./deploy.sh <EC2_IP> <S3_BUCKET> <PEM_KEY>"
  exit 1
fi

echo "=== Deploying DataDoctor AI ==="
echo "EC2: $EC2_IP | S3: $S3_BUCKET"

# ── FRONTEND BUILD ──────────────────────────────────────────────────────────
echo ""
echo "1. Building frontend..."
cd frontend
echo "VITE_API_BASE_URL=http://$EC2_IP:8000/api/v1" > .env.production
npm run build
echo "   Frontend built successfully."

# ── UPLOAD TO S3 ────────────────────────────────────────────────────────────
echo ""
echo "2. Uploading frontend to S3..."
aws s3 sync dist/ s3://$S3_BUCKET/ --delete \
  --cache-control "max-age=31536000" \
  --exclude "index.html"
aws s3 cp dist/index.html s3://$S3_BUCKET/index.html \
  --cache-control "no-cache, no-store, must-revalidate"
echo "   Frontend uploaded to S3."

# ── DEPLOY BACKEND TO EC2 ───────────────────────────────────────────────────
echo ""
echo "3. Deploying backend to EC2..."
cd ../backend

# Copy backend files
ssh -i $PEM_KEY -o StrictHostKeyChecking=no ubuntu@$EC2_IP "mkdir -p /home/ubuntu/datadoctor/app"
scp -i $PEM_KEY -r app/ ubuntu@$EC2_IP:/home/ubuntu/datadoctor/
scp -i $PEM_KEY requirements.txt ubuntu@$EC2_IP:/home/ubuntu/datadoctor/
scp -i $PEM_KEY datadoctor.service ubuntu@$EC2_IP:/tmp/

# Install and start service
ssh -i $PEM_KEY ubuntu@$EC2_IP << 'ENDSSH'
  cd /home/ubuntu/datadoctor
  python3 -m venv venv 2>/dev/null || true
  source venv/bin/activate
  pip install --quiet --upgrade pip
  pip install --quiet -r requirements.txt
  sudo cp /tmp/datadoctor.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable datadoctor
  sudo systemctl restart datadoctor
  echo "Backend service status:"
  sudo systemctl status datadoctor --no-pager
ENDSSH

echo ""
echo "=== Deployment Complete ==="
echo "Frontend: http://$S3_BUCKET.s3-website-us-east-1.amazonaws.com"
echo "Backend:  http://$EC2_IP:8000"
echo "API Docs: http://$EC2_IP:8000/docs"
