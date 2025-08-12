# MongoDB Atlas Setup Guide for Institute Dating Website

## Overview
This guide explains how to set up MongoDB Atlas (cloud database) for the Institute Dating Website. MongoDB Atlas provides a free, cloud-hosted database that's perfect for development and production use.

## Why MongoDB Atlas?
- **Free Tier**: 512MB storage, shared RAM
- **No Installation**: Cloud-hosted, no local setup required
- **Scalability**: Easy to upgrade as your app grows
- **Security**: Built-in security features
- **Backups**: Automatic backups included
- **Monitoring**: Real-time performance monitoring

## Step-by-Step Setup

### Step 1: Create MongoDB Atlas Account
1. **Go to [MongoDB Atlas](https://cloud.mongodb.com/)**
2. **Click "Try Free" or "Sign Up"**
3. **Fill in your details:**
   - Email address
   - Password
   - Account name (e.g., "Suraj Kumar - Institute Dating")

### Step 2: Create Your First Cluster
1. **Choose "FREE" tier (M0)**
   - This gives you 512MB storage
   - Perfect for development and small applications
2. **Select Cloud Provider:**
   - AWS, Google Cloud, or Azure (any one)
   - Choose based on your preference
3. **Choose Region:**
   - Select closest to your location
   - For India: Choose Mumbai or Singapore
4. **Click "Create Cluster"**
   - This may take 2-3 minutes

### Step 3: Configure Database Access
1. **Click "Database Access" in left sidebar**
2. **Click "Add New Database User"**
3. **Create user:**
   - Username: `institute_dating_user`
   - Password: `your_secure_password_here` (save this!)
   - Role: `Read and write to any database`
4. **Click "Add User"**

### Step 4: Configure Network Access
1. **Click "Network Access" in left sidebar**
2. **Click "Add IP Address"**
3. **Choose option:**
   - **For development:** Click "Allow Access from Anywhere" (0.0.0.0/0)
   - **For production:** Add your specific IP addresses
4. **Click "Confirm"**

### Step 5: Get Connection String
1. **Click "Connect" button on your cluster**
2. **Choose "Connect your application"**
3. **Copy the connection string**
4. **Replace `<password>` with your actual password**
5. **Replace `<dbname>` with `institute_dating`

## Application Configuration

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Environment File
1. **Copy `env_example.txt` to `.env`**
2. **Update the connection string:**

```env
# MongoDB Atlas Configuration
MONGO_URI=mongodb+srv://institute_dating_user:your_actual_password@cluster0.mongodb.net/institute_dating?retryWrites=true&w=majority

# Flask Configuration
SECRET_KEY=your-super-secret-key-here-change-this-in-production
FLASK_ENV=development

# Application Configuration
DEBUG=True
```

### Step 3: Update Connection String
Replace the placeholder values in your `.env` file:
- `institute_dating_user` → Your actual username
- `your_actual_password` → Your actual password
- `cluster0.mongodb.net` → Your actual cluster URL

## Database Structure

### Collections Created Automatically
The application will create these collections when you first use them:

#### 1. Users Collection
```json
{
  "_id": ObjectId("..."),
  "username": "john_doe",
  "email": "john@example.com",
  "password_hash": "hashed_password",
  "first_name": "John",
  "last_name": "Doe",
  "age": 22,
  "gender": "male",
  "interested_in": "female",
  "institute": "MIT",
  "course": "Computer Science",
  "year": 3,
  "bio": "I love coding and music",
  "profile_picture": "",
  "location": "Boston, MA",
  "interests": "coding, music, travel",
  "created_at": ISODate("2024-08-12T...")
}
```

#### 2. Likes Collection
```json
{
  "_id": ObjectId("..."),
  "liker_id": ObjectId("user_id"),
  "liked_id": ObjectId("user_id"),
  "timestamp": ISODate("2024-08-12T...")
}
```

#### 3. Messages Collection
```json
{
  "_id": ObjectId("..."),
  "sender_id": ObjectId("user_id"),
  "receiver_id": ObjectId("user_id"),
  "content": "Hello! How are you?",
  "timestamp": ISODate("2024-08-12T..."),
  "is_read": false
}
```

## Running the Application

### Step 1: Start the Application
```bash
python main.py
```

### Step 2: Check Connection
You should see:
```
✅ Environment variables loaded from .env file
✅ MongoDB Atlas connection successful!
   Database: institute_dating
   Collections: []
```

### Step 3: Access the Website
Open your browser and go to `http://localhost:5000`

## MongoDB Atlas Dashboard

### Monitoring Your Database
1. **Log into [MongoDB Atlas](https://cloud.mongodb.com/)**
2. **View your cluster dashboard**
3. **Monitor:**
   - Database performance
   - Storage usage
   - Connection count
   - Query performance

### Database Operations
1. **Browse Collections:**
   - Click on your database
   - View collections and documents
2. **Run Queries:**
   - Use the built-in query interface
   - Test aggregation pipelines

## Troubleshooting

### Common Issues

#### 1. Connection Failed
```
❌ MongoDB Atlas connection failed: [WinError 10061]
```
**Solutions:**
- Check if your IP is whitelisted
- Verify username and password
- Ensure cluster is running

#### 2. Authentication Failed
```
❌ MongoDB Atlas connection failed: Authentication failed
```
**Solutions:**
- Verify database user credentials
- Check if user has correct permissions
- Ensure password is correct

#### 3. Network Access Denied
```
❌ MongoDB Atlas connection failed: Network access denied
```
**Solutions:**
- Add your IP to whitelist
- Use "Allow Access from Anywhere" for development
- Check firewall settings

### Performance Optimization

#### 1. Create Indexes
```javascript
// In MongoDB Atlas dashboard or Compass
db.users.createIndex({"username": 1})
db.users.createIndex({"email": 1})
db.likes.createIndex({"liker_id": 1, "liked_id": 1})
db.messages.createIndex({"sender_id": 1, "receiver_id": 1})
```

#### 2. Monitor Queries
- Use MongoDB Atlas Performance Advisor
- Check slow query logs
- Optimize frequently used queries

## Security Best Practices

### 1. Database Security
- Use strong passwords
- Enable database user authentication
- Regularly rotate credentials

### 2. Network Security
- Limit IP access in production
- Use VPC peering for AWS/Azure
- Enable SSL/TLS encryption

### 3. Application Security
- Store credentials in environment variables
- Never commit `.env` files to version control
- Use HTTPS in production

## Scaling Your Application

### Free Tier Limits
- **Storage:** 512MB
- **RAM:** Shared
- **Connections:** 500

### Upgrading
When you need more resources:
1. **Click "Modify" on your cluster**
2. **Choose higher tier**
3. **Select resources needed**
4. **Confirm changes**

## Backup and Recovery

### Automatic Backups
- MongoDB Atlas provides automatic backups
- Configurable retention periods
- Point-in-time recovery

### Manual Backups
```bash
# Export data
mongodump --uri="mongodb+srv://username:password@cluster.mongodb.net/institute_dating"

# Import data
mongorestore --uri="mongodb+srv://username:password@cluster.mongodb.net/institute_dating"
```

## Support and Resources

### MongoDB Atlas Support
- **Free Tier Support:** Community forums
- **Paid Support:** 24/7 technical support
- **Documentation:** Comprehensive guides

### Useful Links
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [MongoDB University](https://university.mongodb.com/)
- [MongoDB Community Forums](https://www.mongodb.com/community/forums/)

## Next Steps

1. **Set up MongoDB Atlas** using this guide
2. **Configure your application** with the connection string
3. **Test the connection** by running the app
4. **Create your first user** through the registration form
5. **Monitor performance** using Atlas dashboard
6. **Scale as needed** when your app grows

---

**Note**: This setup guide is specifically designed for the Institute Dating Website using MongoDB Atlas. The free tier is perfect for development and can handle thousands of users before needing to upgrade.

**CEO**: Suraj Kumar - Chief Executive Officer
**Project**: Institute Dating Website
**Database**: MongoDB Atlas Cloud
