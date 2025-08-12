# MongoDB Setup Guide for Institute Dating Website

## Overview
This guide explains how to set up MongoDB for the Institute Dating Website. MongoDB is a NoSQL database that provides flexible, scalable data storage.

## Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection for downloading MongoDB

## Installation Options

### Option 1: MongoDB Community Server (Recommended)

#### Windows Installation
1. **Download MongoDB Community Server**:
   - Go to [MongoDB Download Center](https://www.mongodb.com/try/download/community)
   - Select "Windows" and "msi" package
   - Download the latest version

2. **Install MongoDB**:
   - Run the downloaded .msi file
   - Follow the installation wizard
   - Install MongoDB as a service (recommended)
   - Install MongoDB Compass (GUI tool)

3. **Verify Installation**:
   ```bash
   # Check if MongoDB service is running
   services.msc
   # Look for "MongoDB" service
   ```

#### macOS Installation
1. **Using Homebrew**:
   ```bash
   brew tap mongodb/brew
   brew install mongodb-community
   ```

2. **Start MongoDB**:
   ```bash
   brew services start mongodb-community
   ```

#### Linux (Ubuntu) Installation
1. **Import MongoDB GPG key**:
   ```bash
   wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
   ```

2. **Add MongoDB repository**:
   ```bash
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   ```

3. **Install MongoDB**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y mongodb-org
   ```

4. **Start MongoDB**:
   ```bash
   sudo systemctl start mongod
   sudo systemctl enable mongod
   ```

### Option 2: MongoDB Atlas (Cloud Database)

1. **Create MongoDB Atlas Account**:
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for a free account

2. **Create Cluster**:
   - Choose "Free" tier
   - Select cloud provider and region
   - Click "Create Cluster"

3. **Configure Database Access**:
   - Create database user with password
   - Note down username and password

4. **Configure Network Access**:
   - Add your IP address or `0.0.0.0/0` for all IPs

5. **Get Connection String**:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string

## Configuration

### 1. Update Application Configuration
Edit `config.py` to use your MongoDB connection:

```python
# For local MongoDB
MONGO_URI = 'mongodb://localhost:27017/institute_dating'

# For MongoDB Atlas
MONGO_URI = 'mongodb+srv://username:password@cluster.mongodb.net/institute_dating'
```

### 2. Environment Variables (Optional)
Create a `.env` file in your project root:

```env
MONGO_URI=mongodb://localhost:27017/institute_dating
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## Database Structure

### Collections

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

### 1. Start MongoDB
```bash
# Windows (if installed as service)
# MongoDB should start automatically

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### 2. Run Flask Application
```bash
python main.py
```

### 3. Access the Website
Open your browser and go to `http://localhost:5000`

## MongoDB Compass (GUI Tool)

### Installation
- Download from [MongoDB Compass](https://www.mongodb.com/try/download/compass)
- Install and connect to your database

### Features
- Visual database explorer
- Query builder
- Data visualization
- Performance analysis

## Troubleshooting

### Common Issues

#### 1. Connection Refused
```bash
# Check if MongoDB is running
# Windows
services.msc

# macOS/Linux
sudo systemctl status mongod
```

#### 2. Authentication Failed
- Verify username and password
- Check network access settings
- Ensure database user has correct permissions

#### 3. Port Already in Use
```bash
# Check what's using port 27017
netstat -an | grep 27017

# Kill process if needed
sudo kill -9 <process_id>
```

### Performance Optimization

#### 1. Indexes
Create indexes for better query performance:

```javascript
// In MongoDB shell or Compass
db.users.createIndex({"username": 1})
db.users.createIndex({"email": 1})
db.likes.createIndex({"liker_id": 1, "liked_id": 1})
db.messages.createIndex({"sender_id": 1, "receiver_id": 1})
```

#### 2. Connection Pooling
The application automatically handles connection pooling through PyMongo.

## Security Considerations

### 1. Network Security
- Use firewall rules to restrict access
- Enable authentication for production
- Use SSL/TLS encryption

### 2. Data Security
- Hash passwords (already implemented)
- Validate input data
- Implement rate limiting

### 3. Backup Strategy
```bash
# Create backup
mongodump --db institute_dating --out /backup/path

# Restore backup
mongorestore --db institute_dating /backup/path/institute_dating
```

## Monitoring

### 1. MongoDB Logs
```bash
# View logs
tail -f /var/log/mongodb/mongod.log
```

### 2. Performance Metrics
- Use MongoDB Compass for visual monitoring
- Monitor query performance
- Check system resources

## Next Steps

1. **Set up MongoDB** using one of the installation methods
2. **Configure connection** in your application
3. **Test the application** with sample data
4. **Monitor performance** and optimize as needed
5. **Set up backups** for production use

## Support

- [MongoDB Documentation](https://docs.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Flask-PyMongo Documentation](https://flask-pymongo.readthedocs.io/)

---

**Note**: This setup guide is specifically designed for the Institute Dating Website. Adjust configurations based on your specific requirements and environment.
