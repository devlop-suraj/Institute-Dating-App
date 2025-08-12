# Azure Deployment Script for Institute Dating Website
# Run this script in PowerShell as Administrator

Write-Host "🚀 Starting Azure Deployment for Institute Dating Website..." -ForegroundColor Green

# Check if Azure CLI is installed
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✅ Azure CLI found: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not found. Installing..." -ForegroundColor Red
    Write-Host "Installing Azure CLI via winget..." -ForegroundColor Yellow
    winget install Microsoft.AzureCLI
    Write-Host "Please restart PowerShell and run this script again." -ForegroundColor Yellow
    exit
}

# Check if logged in to Azure
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Host "✅ Logged in to Azure as: $($account.user.name)" -ForegroundColor Green
} catch {
    Write-Host "🔐 Please login to Azure..." -ForegroundColor Yellow
    az login
}

# Get subscription
$subscription = az account show --query "id" --output tsv
Write-Host "📋 Using subscription: $subscription" -ForegroundColor Cyan

# Set variables
$resourceGroup = "institute-dating-rg"
$location = "East US"
$appServicePlan = "institute-dating-plan"
$webAppName = "institute-dating-app"
$sku = "F1"

Write-Host "🏗️  Creating Resource Group: $resourceGroup" -ForegroundColor Yellow
az group create --name $resourceGroup --location $location

Write-Host "📋 Creating App Service Plan: $appServicePlan" -ForegroundColor Yellow
az appservice plan create --name $appServicePlan --resource-group $resourceGroup --sku $sku --is-linux

Write-Host "🌐 Creating Web App: $webAppName" -ForegroundColor Yellow
az webapp create --resource-group $resourceGroup --plan $appServicePlan --name $webAppName --runtime "PYTHON:3.11"

Write-Host "⚙️  Configuring environment variables..." -ForegroundColor Yellow

# Get MongoDB URI from user
$mongoUri = Read-Host "Enter your MongoDB Atlas connection string"
$secretKey = Read-Host "Enter a secret key for Flask sessions (or press Enter to generate one)"

if ([string]::IsNullOrEmpty($secretKey)) {
    $secretKey = [System.Web.Security.Membership]::GeneratePassword(32, 10)
    Write-Host "Generated secret key: $secretKey" -ForegroundColor Cyan
}

# Set environment variables
az webapp config appsettings set --resource-group $resourceGroup --name $webAppName --settings MONGODB_URI="$mongoUri"
az webapp config appsettings set --resource-group $resourceGroup --name $webAppName --settings SECRET_KEY="$secretKey"
az webapp config appsettings set --resource-group $resourceGroup --name $webAppName --settings MAIL_SERVER="smtp.gmail.com"
az webapp config appsettings set --resource-group $resourceGroup --name $webAppName --settings MAIL_PORT="587"
az webapp config appsettings set --resource-group $resourceGroup --name $webAppName --settings MAIL_USE_TLS="True"
az webapp config appsettings set --resource-group $resourceGroup --name $webAppName --settings MAIL_USERNAME="surajkumarch110@gmail.com"
az webapp config appsettings set --resource-group $resourceGroup --name $webAppName --settings MAIL_PASSWORD="tkna qlfx bouq olwm"

Write-Host "📁 Setting up Git deployment..." -ForegroundColor Yellow

# Initialize git if not already done
if (-not (Test-Path ".git")) {
    git init
    git add .
    git commit -m "Initial commit for Azure deployment"
}

# Configure Azure deployment
$deploymentUrl = az webapp deployment source config-local-git --resource-group $resourceGroup --name $webAppName --query url --output tsv

Write-Host "🔗 Adding Azure remote..." -ForegroundColor Yellow
git remote remove azure 2>$null
git remote add azure $deploymentUrl

Write-Host "📤 Deploying to Azure..." -ForegroundColor Yellow
git push azure main

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host "🌐 Your app is available at: https://$webAppName.azurewebsites.net" -ForegroundColor Cyan

Write-Host "📊 To monitor your app:" -ForegroundColor Yellow
Write-Host "   az webapp log tail --resource-group $resourceGroup --name $webAppName" -ForegroundColor White

Write-Host "🔧 To update environment variables:" -ForegroundColor Yellow
Write-Host "   az webapp config appsettings set --resource-group $resourceGroup --name $webAppName --settings KEY=VALUE" -ForegroundColor White

Write-Host "🗑️  To clean up resources (when no longer needed):" -ForegroundColor Yellow
Write-Host "   az group delete --name $resourceGroup --yes" -ForegroundColor White
