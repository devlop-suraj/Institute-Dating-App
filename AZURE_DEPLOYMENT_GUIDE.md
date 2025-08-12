# Azure Deployment Guide for Institute Dating Website

## Prerequisites
- Microsoft Azure account (free tier available)
- Azure CLI installed on your computer
- Git installed on your computer

## Option 1: Azure App Service (Easiest - Recommended)

### Step 1: Install Azure CLI
```bash
# Download and install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
# Or use winget on Windows:
winget install Microsoft.AzureCLI
```

### Step 2: Login to Azure
```bash
az login
# This will open a browser window for authentication
```

### Step 3: Create Resource Group
```bash
az group create --name "institute-dating-rg" --location "East US"
```

### Step 4: Create App Service Plan
```bash
az appservice plan create --name "institute-dating-plan" --resource-group "institute-dating-rg" --sku "F1" --is-linux
```

### Step 5: Create Web App
```bash
az webapp create --resource-group "institute-dating-rg" --plan "institute-dating-plan" --name "institute-dating-app" --runtime "PYTHON:3.11"
```

### Step 6: Configure Environment Variables
```bash
# Set your MongoDB connection string
az webapp config appsettings set --resource-group "institute-dating-rg" --name "institute-dating-app" --settings MONGODB_URI="your_mongodb_atlas_connection_string"

# Set your email configuration
az webapp config appsettings set --resource-group "institute-dating-rg" --name "institute-dating-app" --settings MAIL_SERVER="smtp.gmail.com"
az webapp config appsettings set --resource-group "institute-dating-rg" --name "institute-dating-app" --settings MAIL_PORT="587"
az webapp config appsettings set --resource-group "institute-dating-rg" --name "institute-dating-app" --settings MAIL_USE_TLS="True"
az webapp config appsettings set --resource-group "institute-dating-rg" --name "institute-dating-app" --settings MAIL_USERNAME="surajkumarch110@gmail.com"
az webapp config appsettings set --resource-group "institute-dating-rg" --name "institute-dating-app" --settings MAIL_PASSWORD="tkna qlfx bouq olwm"
az webapp config appsettings set --resource-group "institute-dating-rg" --name "institute-dating-app" --settings SECRET_KEY="your_secret_key_here"
```

### Step 7: Deploy Your Code
```bash
# Navigate to your project directory
cd "C:\Users\shurj\Programming\GEN_AI\Capital one"

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Azure deployment"

# Add Azure remote
az webapp deployment source config-local-git --resource-group "institute-dating-rg" --name "institute-dating-app"

# Get the git remote URL
az webapp deployment source config-local-git --resource-group "institute-dating-rg" --name "institute-dating-app" --query url --output tsv

# Add the remote and push
git remote add azure <URL_FROM_ABOVE>
git push azure main
```

### Step 8: Access Your App
Your app will be available at: `https://institute-dating-app.azurewebsites.net`

## Option 2: Azure Container Instances (More Advanced)

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "600", "main:app"]
```

### Step 2: Build and Deploy
```bash
# Build Docker image
docker build -t institute-dating .

# Login to Azure Container Registry
az acr login --name yourregistryname

# Tag and push image
docker tag institute-dating yourregistryname.azurecr.io/institute-dating:latest
docker push yourregistryname.azurecr.io/institute-dating:latest

# Deploy to Container Instances
az container create --resource-group "institute-dating-rg" --name "institute-dating-container" --image yourregistryname.azurecr.io/institute-dating:latest --dns-name-label "institute-dating" --ports 8000
```

## Option 3: Azure Virtual Machines (Most Control)

### Step 1: Create VM
```bash
az vm create --resource-group "institute-dating-rg" --name "institute-dating-vm" --image "Ubuntu2204" --admin-username azureuser --generate-ssh-keys
```

### Step 2: Open Ports
```bash
az vm open-port --resource-group "institute-dating-rg" --name "institute-dating-vm" --port 80
az vm open-port --resource-group "institute-dating-rg" --name "institute-dating-vm" --port 443
```

### Step 3: SSH and Setup
```bash
# SSH into your VM
ssh azureuser@<VM_PUBLIC_IP>

# Install dependencies
sudo apt update
sudo apt install python3 python3-pip nginx

# Clone your code and setup
git clone <your-repo>
cd <your-project>
pip3 install -r requirements.txt

# Setup systemd service
sudo nano /etc/systemd/system/institute-dating.service
```

### Step 4: Systemd Service File
```ini
[Unit]
Description=Institute Dating Website
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/<your-project>
Environment="PATH=/home/azureuser/<your-project>/venv/bin"
ExecStart=/home/azureuser/<your-project>/venv/bin/gunicorn --bind 0.0.0.0:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## Important Configuration Notes

### 1. Environment Variables
Make sure to set these in Azure App Service Configuration:
- `MONGODB_URI`: Your MongoDB Atlas connection string
- `SECRET_KEY`: A secure random string for Flask sessions
- `MAIL_*`: Email configuration for password reset and notifications

### 2. CORS and Security
If you plan to have a separate frontend, configure CORS:
```python
from flask_cors import CORS
CORS(app, origins=["https://yourdomain.com"])
```

### 3. Custom Domain
```bash
# Add custom domain
az webapp config hostname add --webapp-name "institute-dating-app" --resource-group "institute-dating-rg" --hostname "dating.yourinstitute.com"
```

### 4. SSL Certificate
Azure App Service automatically provides SSL certificates for `*.azurewebsites.net` domains.

## Monitoring and Scaling

### 1. Application Insights
```bash
# Enable Application Insights
az monitor app-insights component create --app "institute-dating-insights" --location "East US" --resource-group "institute-dating-rg" --application-type web
```

### 2. Scaling
```bash
# Scale up (change plan)
az appservice plan update --name "institute-dating-plan" --resource-group "institute-dating-rg" --sku "S1"

# Enable auto-scaling
az monitor autoscale create --resource-group "institute-dating-rg" --resource "institute-dating-plan" --resource-type "Microsoft.Web/serverfarms" --name "institute-dating-autoscale" --min-count 1 --max-count 10 --count 1
```

## Cost Estimation (Free Tier)
- **App Service Plan F1**: Free (1 GB RAM, shared CPU)
- **Bandwidth**: 1 GB/month free
- **Storage**: 1 GB free
- **Custom Domain**: Free (but domain registration costs extra)

## Troubleshooting

### Common Issues:
1. **Module not found errors**: Check requirements.txt and runtime.txt
2. **Connection refused**: Verify MongoDB Atlas IP whitelist includes Azure IPs
3. **Environment variables**: Ensure all required variables are set in App Service Configuration
4. **Port binding**: Use `0.0.0.0` instead of `localhost` in production

### Logs:
```bash
# View application logs
az webapp log tail --resource-group "institute-dating-rg" --name "institute-dating-app"
```

## Next Steps After Deployment

1. **Test all functionality** on the live site
2. **Set up monitoring** with Application Insights
3. **Configure backup** for your MongoDB Atlas database
4. **Set up CI/CD** pipeline for automatic deployments
5. **Monitor costs** and optimize resources

## Support Resources

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Azure Python Documentation](https://docs.microsoft.com/en-us/azure/developer/python/)
- [Azure Community Support](https://docs.microsoft.com/en-us/answers/topics/azure-python.html)
