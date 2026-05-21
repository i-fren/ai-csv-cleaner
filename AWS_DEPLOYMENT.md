# DataDoctor AI — AWS Free Tier Deployment Guide

## Architecture
```
Users → S3 Static Website (React frontend)
              ↓ API calls
         EC2 t2.micro (FastAPI backend, port 8000)
```

---

## Step 1 — Create an EC2 Instance

1. Go to **AWS Console → EC2 → Launch Instance**
2. Settings:
   - **Name**: `datadoctor-backend`
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance type**: `t2.micro` (Free tier)
   - **Key pair**: Create new → download `.pem` file → save it safely
   - **Security Group** — Add these inbound rules:
     | Type | Port | Source |
     |------|------|--------|
     | SSH | 22 | My IP |
     | Custom TCP | 8000 | 0.0.0.0/0 |
   - **Storage**: 8 GB gp2 (Free tier)
3. Click **Launch Instance**
4. Note your **Public IPv4 address** (e.g., `54.123.45.67`)

---

## Step 2 — Deploy Backend to EC2

Open a terminal on your Windows machine (Git Bash or WSL):

```bash
# Make the key file secure
chmod 400 /path/to/your-key.pem

# SSH into your EC2 instance
ssh -i /path/to/your-key.pem ubuntu@YOUR_EC2_IP
```

Once connected, run these commands on the EC2:

```bash
# Update and install Python
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv

# Create app directory
mkdir -p /home/ubuntu/datadoctor
cd /home/ubuntu/datadoctor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi "uvicorn[standard]" pandas scikit-learn openai reportlab python-multipart numpy
```

Now **upload your backend code** from your Windows machine (open a new terminal):

```bash
# Copy backend files to EC2
scp -i /path/to/your-key.pem -r f:/csv-cleaner-app/backend/app ubuntu@YOUR_EC2_IP:/home/ubuntu/datadoctor/
scp -i /path/to/your-key.pem f:/csv-cleaner-app/backend/requirements.txt ubuntu@YOUR_EC2_IP:/home/ubuntu/datadoctor/
scp -i /path/to/your-key.pem f:/csv-cleaner-app/backend/datadoctor.service ubuntu@YOUR_EC2_IP:/tmp/
```

Back on the EC2, set up the systemd service:

```bash
# Edit the service file to add your OpenAI key (optional)
sudo nano /tmp/datadoctor.service
# Change: Environment="OPENAI_API_KEY=your_actual_key_here"

# Install and start the service
sudo cp /tmp/datadoctor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable datadoctor
sudo systemctl start datadoctor

# Check it's running
sudo systemctl status datadoctor

# Test the API
curl http://localhost:8000/health
```

You should see: `{"status":"ok"}`

Test from your browser: `http://YOUR_EC2_IP:8000/docs`

---

## Step 3 — Create S3 Bucket for Frontend

1. Go to **AWS Console → S3 → Create Bucket**
2. Settings:
   - **Bucket name**: `datadoctor-frontend` (must be globally unique)
   - **Region**: Same as your EC2 (e.g., us-east-1)
   - **Uncheck** "Block all public access"
   - Check the acknowledgment box
3. After creation, go to **Properties → Static website hosting**:
   - Enable it
   - Index document: `index.html`
   - Error document: `index.html`
4. Go to **Permissions → Bucket Policy** and paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }
  ]
}
```

---

## Step 4 — Build and Upload Frontend

On your Windows machine:

```bash
cd f:/csv-cleaner-app/frontend

# Set your EC2 IP in the production env file
# Edit .env.production and replace YOUR_EC2_PUBLIC_IP with your actual IP

# Build the frontend
npm run build
```

Upload to S3 (install AWS CLI first if needed: https://aws.amazon.com/cli/):

```bash
# Configure AWS CLI (one time)
aws configure
# Enter: Access Key ID, Secret Access Key, Region (e.g., us-east-1), output format (json)

# Upload to S3
aws s3 sync dist/ s3://YOUR_BUCKET_NAME/ --delete
```

---

## Step 5 — Access Your App

- **Frontend**: `http://YOUR_BUCKET_NAME.s3-website-us-east-1.amazonaws.com`
- **Backend API**: `http://YOUR_EC2_IP:8000`
- **API Docs**: `http://YOUR_EC2_IP:8000/docs`

---

## Useful Commands

```bash
# Check backend logs
sudo journalctl -u datadoctor -f

# Restart backend after code changes
sudo systemctl restart datadoctor

# Stop backend
sudo systemctl stop datadoctor

# Update backend code (from Windows)
scp -i key.pem -r f:/csv-cleaner-app/backend/app ubuntu@EC2_IP:/home/ubuntu/datadoctor/
ssh -i key.pem ubuntu@EC2_IP "sudo systemctl restart datadoctor"
```

---

## Cost Estimate (Free Tier)

| Service | Free Tier | After Free Tier |
|---------|-----------|-----------------|
| EC2 t2.micro | 750 hrs/month FREE (12 months) | ~$8.50/month |
| S3 Storage | 5 GB FREE | ~$0.023/GB |
| S3 Requests | 20K GET FREE | ~$0.0004/1K |
| Data Transfer | 1 GB/month FREE | ~$0.09/GB |

**Total cost for demo/hackathon: $0** (within free tier limits)

---

## Troubleshooting

**Backend not accessible?**
- Check EC2 Security Group has port 8000 open to 0.0.0.0/0
- Run: `sudo systemctl status datadoctor`
- Check logs: `sudo journalctl -u datadoctor -n 50`

**CORS errors in browser?**
- The backend already allows all origins. If issues persist, check the EC2 IP in `.env.production` matches exactly.

**Frontend shows blank page?**
- Check S3 bucket policy is set correctly
- Check Static Website Hosting is enabled
- Make sure `index.html` is the index document

**ML training fails?**
- t2.micro has 1 GB RAM — large datasets (>50K rows) may be slow. This is normal.
