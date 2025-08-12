# Institute Dating Website 💕

एक modern dating website जो institute के students के लिए बनाया गया है। यह website students को अपने academic community में meaningful relationships बनाने में help करता है।

## Features ✨

### 🔐 User Authentication
- User registration और login system
- Secure password hashing
- Session management

### 👤 Profile Management
- Complete user profiles with academic information
- Institute, course, year of study details
- Bio, interests, और location
- Profile editing capabilities

### 💘 Matching System
- Like/dislike functionality
- Mutual matching algorithm
- Dashboard with potential matches
- Match notifications

### 💬 Chat System
- Real-time messaging between matched users
- Chat interface with message history
- User-friendly conversation flow

### 🎨 Modern UI/UX
- Responsive design for all devices
- Beautiful gradient backgrounds
- Interactive elements और animations
- Bootstrap 5 framework

## Installation 🚀

### Prerequisites
- Python 3.8 या higher
- pip package manager

### Setup Steps

1. **Clone या download करें:**
   ```bash
   git clone <repository-url>
   cd institute-dating
   ```

2. **Virtual environment create करें:**
   ```bash
   python -m venv venv
   
   # Windows पर
   venv\Scripts\activate
   
   # Linux/Mac पर
   source venv/bin/activate
   ```

3. **Dependencies install करें:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Application run करें:**
   ```bash
   python main.py
   ```

5. **Browser में जाएं:**
   ```
   http://localhost:5000
   ```

## Usage 📱

### For New Users
1. **Register करें** - अपना profile create करें
2. **Profile complete करें** - bio, interests add करें
3. **Browse profiles** - potential matches देखें
4. **Send likes** - interested users को like करें

### For Existing Users
1. **Login करें** - अपने account में जाएं
2. **Dashboard** - new matches देखें
3. **Chat** - matched users से बात करें
4. **Profile update** - अपनी information update करें

## Database Schema 🗄️

### Users Table
- Basic info: username, email, password
- Personal details: name, age, gender
- Academic info: institute, course, year
- Profile data: bio, location, interests

### Messages Table
- Sender और receiver IDs
- Message content और timestamp
- Read status tracking

### Likes Table
- Liker और liked user IDs
- Timestamp for like activity

## Security Features 🔒

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection
- Input validation
- SQL injection prevention

## Customization 🎨

### Colors
Website के colors को customize करने के लिए `templates/base.html` में CSS variables edit करें:

```css
:root {
    --primary-color: #ff6b9d;
    --secondary-color: #4ecdc4;
    --accent-color: #45b7d1;
}
```

### Institute Specific Features
- Institute names को customize करें
- Course categories add करें
- Year ranges modify करें

## Future Enhancements 🚀

- [ ] Profile pictures support
- [ ] Advanced matching algorithms
- [ ] Push notifications
- [ ] Video chat integration
- [ ] Mobile app development
- [ ] Admin panel
- [ ] Analytics dashboard

## Contributing 🤝

1. Fork करें
2. Feature branch create करें
3. Changes commit करें
4. Pull request submit करें

## License 📄

This project is open source और MIT License के under available है।

## Support 💬

अगर कोई questions या issues हैं तो:
- Issue create करें
- Documentation check करें
- Community में help लें

---

**Made with ❤️ for students to find meaningful connections!**
