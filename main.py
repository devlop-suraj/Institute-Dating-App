from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import os
from datetime import datetime, timezone
import random
from bson import ObjectId
from PIL import Image
import io
from config import config

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Or set environment variables manually")

app = Flask(__name__)

# Configuration
config_name = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

# File upload configuration - use config values
UPLOAD_FOLDER = app.config.get('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024)  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Email configuration for password reset
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'surajkumarch110@gmail.com'
app.config['MAIL_PASSWORD'] = 'tkna qlfx bouq olwm'
app.config['MAIL_DEFAULT_SENDER'] = 'surajkumarch110@gmail.com'

# Initialize Flask-Mail
mail = Mail(app)

# Initialize serializer for password reset tokens
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# MongoDB Atlas Configuration
try:
    mongo = PyMongo(app)
    # Test connection to MongoDB Atlas
    mongo.db.command('ping')
    print("✅ MongoDB Atlas connection successful!")
    print(f"   Database: {mongo.db.name}")
    print(f"   Collections: {mongo.db.list_collection_names()}")
except Exception as e:
    print(f"❌ MongoDB Atlas connection failed: {e}")
    print("Please ensure:")
    print("1. MongoDB Atlas cluster is running")
    print("2. Network access is configured (IP whitelist)")
    print("3. Database user credentials are correct")
    print("4. Connection string is properly formatted")
    print("\nCheck MONGODB_SETUP.md for detailed setup instructions")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_picture(file, user_id):
    """Save and process profile picture"""
    try:
        # Create filename
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"profile_{user_id}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Open and process image
        image = Image.open(file.stream)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image to reasonable dimensions (300x300)
        image.thumbnail((300, 300), Image.Resampling.LANCZOS)
        
        # Save processed image
        image.save(filepath, 'JPEG', quality=85, optimize=True)
        
        return filename
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def send_password_reset_email(email, reset_url):
    """Send password reset email"""
    try:
        msg = Message(
            'Password Reset Request - Institute Dating',
            recipients=[email],
            body=f'''Hello!

You have requested to reset your password for your Institute Dating account.

To reset your password, visit the following link:
{reset_url}

This link will expire in 1 hour.

If you did not request this password reset, please ignore this email.

Best regards,
Institute Dating Team
Founded by Suraj Kumar - CEO
''',
            html=f'''
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #667eea;">Password Reset Request</h2>
                <p>Hello!</p>
                <p>You have requested to reset your password for your <strong>Institute Dating</strong> account.</p>
                <p>To reset your password, click the button below:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a>
                </div>
                <p><strong>Note:</strong> This link will expire in 1 hour.</p>
                <p>If you did not request this password reset, please ignore this email.</p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">
                    Best regards,<br>
                    <strong>Institute Dating Team</strong><br>
                    Founded by <strong>Suraj Kumar</strong> - CEO
                </p>
            </div>
            '''
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_signup_confirmation_email(email, username, user_id, first_name, last_name):
    """Send signup confirmation email with user ID"""
    try:
        msg = Message(
            'Welcome to Institute Dating! 🎉 - Signup Confirmation',
            recipients=[email],
            body=f'''Congratulations {first_name} {last_name}!

Welcome to Institute Dating! 🎉

Your account has been successfully created with the following details:

Username: {username}
User ID: {user_id}

You can now login to your account and start exploring potential matches from your institute!

Best regards,
Institute Dating Team
Founded by Suraj Kumar - CEO
''',
            html=f'''
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px;">
                <div style="background: white; padding: 30px; border-radius: 10px; text-align: center;">
                    <h1 style="color: #667eea; margin-bottom: 20px;">🎉 Welcome to Institute Dating! 🎉</h1>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea;">
                        <h3 style="color: #333; margin-bottom: 15px;">Account Details</h3>
                        <p style="font-size: 16px; margin: 8px 0;"><strong>Username:</strong> <span style="color: #667eea;">{username}</span></p>
                        <p style="font-size: 16px; margin: 8px 0;"><strong>User ID:</strong> <span style="color: #667eea; font-family: monospace;">{user_id}</span></p>
                        <p style="font-size: 16px; margin: 8px 0;"><strong>Name:</strong> <span style="color: #667eea;">{first_name} {last_name}</span></p>
                    </div>
                    
                    <p style="font-size: 18px; color: #333; margin: 20px 0;">
                        Your account has been successfully created! 🎊
                    </p>
                    
                    <p style="font-size: 16px; color: #666; margin: 15px 0;">
                        You can now login to your account and start exploring potential matches from your institute!
                    </p>
                    
                    <div style="margin: 30px 0;">
                        <a href="http://localhost:5000/login" style="background: #667eea; color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; display: inline-block; font-size: 16px; font-weight: bold; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                            🚀 Login Now
                        </a>
                    </div>
                    
                    <div style="background: #e8f4fd; padding: 15px; border-radius: 8px; margin: 20px 0; border: 1px solid #bee5eb;">
                        <p style="margin: 0; color: #0c5460; font-size: 14px;">
                            <strong>💡 Tip:</strong> Complete your profile to get better matches and increase your compatibility score!
                        </p>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 20px;">
                    <p style="color: white; font-size: 14px; margin: 0;">
                        Best regards,<br>
                        <strong>Institute Dating Team</strong><br>
                        Founded by <strong>Suraj Kumar</strong> - CEO
                    </p>
                </div>
            </div>
            '''
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending signup confirmation email: {e}")
        return False

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.password_hash = user_data['password_hash']
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.age = user_data['age']
        self.gender = user_data['gender']
        self.interested_in = user_data['interested_in']
        self.institute = user_data['institute']
        self.course = user_data['course']
        self.year = user_data['year']
        self.bio = user_data.get('bio', '')
        self.profile_picture = user_data.get('profile_picture', '')
        self.location = user_data.get('location', '')
        self.building_block = user_data.get('building_block', '')
        self.interests = user_data.get('interests', [])
        self.study_habits = user_data.get('study_habits', [])
        self.personality_type = user_data.get('personality_type', '')
        self.life_goals = user_data.get('life_goals', [])
        self.compatibility_score = user_data.get('compatibility_score', 0)
        self.created_at = user_data.get('created_at', datetime.now(timezone.utc))
        self.unread_notifications = user_data.get('unread_notifications', 0)
        
        # Calculate compatibility score
        self.calculate_compatibility_score()

    def get_id(self):
        return str(self.id)
    
    def calculate_compatibility_score(self):
        """Calculate compatibility score based on profile completeness"""
        score = 0
        if self.bio: score += 10
        if self.interests: score += len(self.interests) * 5
        if self.location: score += 10
        if self.building_block: score += 10
        if self.study_habits: score += len(self.study_habits) * 5
        if self.personality_type: score += 10
        if self.life_goals: score += len(self.life_goals) * 5
        if self.profile_picture: score += 15  # Bonus for profile picture
        self.compatibility_score = min(score, 100)

@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

# Add profile picture upload route
@app.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    try:
        if 'profile_picture' not in request.files:
            return jsonify({'success': False, 'message': 'No file selected'})
        
        file = request.files['profile_picture']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if file and allowed_file(file.filename):
            # Delete old profile picture if exists
            if current_user.profile_picture:
                old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], current_user.profile_picture)
                if os.path.exists(old_filepath):
                    os.remove(old_filepath)
            
            # Save new profile picture
            filename = save_profile_picture(file, current_user.id)
            if filename:
                # Update database
                mongo.db.users.update_one(
                    {'_id': ObjectId(current_user.id)},
                    {'$set': {'profile_picture': filename}}
                )
                
                # Update current user object
                current_user.profile_picture = filename
                current_user.calculate_compatibility_score()
                
                return jsonify({
                    'success': True, 
                    'message': 'Profile picture updated successfully!',
                    'filename': filename,
                    'compatibility_score': current_user.compatibility_score
                })
            else:
                return jsonify({'success': False, 'message': 'Error processing image'})
        else:
            return jsonify({'success': False, 'message': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory('static', filename)

# Add forgot password routes
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Please enter your email address', 'error')
            return render_template('forgot_password.html')
        
        # Check if user exists
        user_data = mongo.db.users.find_one({'email': email})
        if not user_data:
            flash('No account found with that email address', 'error')
            return render_template('forgot_password.html')
        
        # Generate reset token
        token = serializer.dumps(email, salt='password-reset-salt')
        
        # Create reset URL
        reset_url = url_for('reset_password', token=token, _external=True)
        
        # Send email
        if send_password_reset_email(email, reset_url):
            flash('Password reset instructions have been sent to your email', 'success')
        else:
            flash('Error sending email. Please try again later.', 'error')
        
        return render_template('forgot_password.html')
    
    return render_template('forgot_password.html')

@app.route('/forgot_username', methods=['GET', 'POST'])
def forgot_username():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Please enter your email address', 'error')
            return render_template('forgot_username.html')
        
        # Check if user exists
        user_data = mongo.db.users.find_one({'email': email})
        if not user_data:
            flash('No account found with that email address', 'error')
            return render_template('forgot_username.html')
        
        # Show username directly without verification
        return render_template('forgot_username.html', user_data=user_data, email=email)
    
    return render_template('forgot_username.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Verify token (expires in 1 hour)
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or not confirm_password:
            flash('Please fill in all fields', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
        else:
            # Update password
            mongo.db.users.update_one(
                {'email': email},
                {'$set': {'password_hash': generate_password_hash(password)}}
            )
            
            flash('Your password has been updated successfully!', 'success')
            return redirect(url_for('login'))
    
    return render_template('reset_password.html')

# Add compatibility calculation function
def calculate_compatibility(user1, user2):
    """Calculate compatibility score between two users"""
    score = 0
    
    # Interest matching (35 points) - Increased importance
    if user1.interests and user2.interests:
        common_interests = set(interest.strip().lower() for interest in user1.interests) & set(interest.strip().lower() for interest in user2.interests)
        if common_interests:
            score += min(len(common_interests) * 12, 35)
    
    # Study habits compatibility (25 points) - Increased importance
    if user1.study_habits and user2.study_habits:
        common_habits = set(habit.strip().lower() for habit in user1.study_habits) & set(habit.strip().lower() for habit in user2.study_habits)
        if common_habits:
            score += min(len(common_habits) * 8, 25)
    
    # Life goals compatibility (20 points) - New high priority
    if user1.life_goals and user2.life_goals:
        common_goals = set(goal.strip().lower() for goal in user1.life_goals) & set(goal.strip().lower() for goal in user2.life_goals)
        if common_goals:
            score += min(len(common_goals) * 10, 20)
    
    # Bio compatibility (15 points) - New field for text similarity
    if user1.bio and user2.bio:
        # Simple keyword matching for bio compatibility
        bio1_words = set(user1.bio.lower().split())
        bio2_words = set(user2.bio.lower().split())
        common_bio_words = bio1_words & bio2_words
        if len(common_bio_words) >= 3:  # At least 3 common words
            score += 15
        elif len(common_bio_words) >= 1:  # At least 1 common word
            score += 8
    
    # Location matching (15 points) - Reduced importance
    if user1.location and user2.location and user1.location == user2.location:
        score += 15
    
    # Course compatibility (10 points) - Reduced importance
    if user1.course == user2.course:
        score += 10
    elif user1.course and user2.course:
        # Similar fields get partial points
        similar_courses = {
            '(B.Tech)': ['(M.Tech)', '(B.S)'],
            '(M.Tech)': ['(B.Tech)', '(Ph.D)'],
            '(B.S)': ['(B.Tech)', '(M.Sc)'],
            '(M.Sc)': ['(B.S)', '(Ph.D)'],
            '(MBA)': ['(B.Tech)', '(M.Tech)'],
            '(Ph.D)': ['(M.Tech)', '(M.Sc)'],
            'Humanities': ['(B.S)', '(M.Sc)'],
            'OTHERs': ['(B.Tech)', '(M.Sc)', 'Humanities']
        }
        if user1.course in similar_courses and user2.course in similar_courses[user1.course]:
            score += 7
    
    # Year compatibility (8 points) - Reduced importance
    year_diff = abs(int(user1.year) - int(user2.year))
    if year_diff == 0:
        score += 8
    elif year_diff == 1:
        score += 6
    elif year_diff == 2:
        score += 4
    
    # Personality compatibility (12 points) - Reduced importance
    if user1.personality_type and user2.personality_type:
        compatible_pairs = [
            ('Introvert', 'Extrovert'),
            ('Analytical', 'Creative'),
            ('Adventurous', 'Cautious')
        ]
        if (user1.personality_type, user2.personality_type) in compatible_pairs or (user2.personality_type, user1.personality_type) in compatible_pairs:
            score += 12
        elif user1.personality_type == user2.personality_type:
            score += 8
    
    return min(score, 100)

# Add template function for compatibility calculation
@app.template_filter('calculateCompatibility')
def calculate_compatibility_filter(user1, user2):
    return calculate_compatibility(user1, user2)

@app.route('/suggest_matches')
@login_required
def suggest_matches():
    """Suggest additional matches for users who might not have any"""
    try:
        # Get users who haven't been liked by current user
        liked_users = mongo.db.likes.find({'liker_id': ObjectId(current_user.id)})
        liked_user_ids = [like['liked_id'] for like in liked_users]
        
        # Find users with similar interests and compatibility
        suggested_matches = []
        all_users = mongo.db.users.find({
            '_id': {'$ne': ObjectId(current_user.id)},
            '_id': {'$nin': liked_user_ids}
        })
        
        for user_data in all_users:
            user = User(user_data)
            compatibility = calculate_compatibility(current_user, user)
            user.compatibility_score = compatibility
            
            # Only suggest if compatibility is above threshold
            if compatibility >= 30:  # Minimum 30% compatibility
                suggested_matches.append(user)
        
        # Sort by compatibility score
        suggested_matches.sort(key=lambda x: x.compatibility_score, reverse=True)
        
        return jsonify({
            'success': True,
            'suggested_matches': [
                {
                    'id': str(user.id),
                    'name': f"{user.first_name} {user.last_name}",
                    'compatibility': user.compatibility_score,
                    'course': user.course,
                    'year': user.year,
                    'location': user.location,
                    'personality': user.personality_type
                }
                for user in suggested_matches[:5]  # Top 5 suggestions
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = int(request.form['age'])
            gender = request.form['gender']
            interested_in = request.form['interested_in']
            institute = request.form['institute']
            course = request.form['course']
            year = int(request.form['year'])
            
            # Validate email domain
            if not email.endswith('@smail.iitm.ac.in'):
                flash('Please use your @smail.iitm.ac.in email address', 'error')
                return render_template('register.html')
            
            # Check if username or email already exists
            if mongo.db.users.find_one({'username': username}):
                flash('Username already exists!', 'error')
                return render_template('register.html')
            
            if mongo.db.users.find_one({'email': email}):
                flash('Email already exists!', 'error')
                return render_template('register.html')
            
            # Create new user document with minimal required fields
            user_data = {
                'username': username,
                'email': email,
                'password_hash': generate_password_hash(password),
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'gender': gender,
                'interested_in': interested_in,
                'institute': institute,
                'course': course,
                'year': year,
                # Optional fields - can be filled later
                'bio': '',
                'profile_picture': '',
                'location': '',
                'building_block': '',
                'interests': [],
                'study_habits': [],
                'personality_type': '',
                'life_goals': [],
                'compatibility_score': 0,
                'created_at': datetime.now(timezone.utc)
            }
            
            result = mongo.db.users.insert_one(user_data)
            
            # Send signup confirmation email
            send_signup_confirmation_email(email, username, str(result.inserted_id), first_name, last_name)
            
            flash('Registration successful! Please login and complete your profile for better matches.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            # Find user by username
            user_data = mongo.db.users.find_one({'username': username})
            
            if user_data and check_password_hash(user_data['password_hash'], password):
                user = User(user_data)
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password!', 'error')
        except Exception as e:
            flash(f'Login failed: {str(e)}', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        # Get potential matches based on gender preferences
        potential_matches = []
        users_cursor = mongo.db.users.find({
            '_id': {'$ne': ObjectId(current_user.id)},
            'gender': current_user.interested_in,
            'interested_in': current_user.gender
        })
        
        for user_data in users_cursor:
            user = User(user_data)
            # Calculate compatibility score for this user
            compatibility = calculate_compatibility(current_user, user)
            user.compatibility_score = compatibility
            potential_matches.append(user)
        
        # Sort by compatibility score (highest first) to show best matches first
        potential_matches.sort(key=lambda x: x.compatibility_score, reverse=True)
        
        # If no matches found, try to find users with similar interests regardless of gender
        if not potential_matches:
            fallback_users = mongo.db.users.find({
                '_id': {'$ne': ObjectId(current_user.id)}
            })
            
            for user_data in fallback_users:
                user = User(user_data)
                compatibility = calculate_compatibility(current_user, user)
                user.compatibility_score = compatibility
                potential_matches.append(user)
            
            # Sort by compatibility score
            potential_matches.sort(key=lambda x: x.compatibility_score, reverse=True)
        
        # Additional sorting: prioritize users with complete profiles (interests, study habits, life goals, bio)
        def profile_completeness_score(user):
            score = 0
            if user.interests: score += 1
            if user.study_habits: score += 1
            if user.life_goals: score += 1
            if user.bio: score += 1
            return score
        
        # Sort by compatibility first, then by profile completeness
        potential_matches.sort(key=lambda x: (x.compatibility_score, profile_completeness_score(x)), reverse=True)
        
        return render_template('dashboard.html', potential_matches=potential_matches)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('dashboard.html', potential_matches=[])

@app.route('/profile/<user_id>')
@login_required
def profile(user_id):
    try:
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user_data:
            flash('User not found!', 'error')
            return redirect(url_for('dashboard'))
        
        user = User(user_data)
        
        # Check if current user has liked this profile
        has_liked = mongo.db.likes.find_one({
            'liker_id': ObjectId(current_user.id),
            'liked_id': ObjectId(user_id)
        })
        
        # Check if this is a mutual match
        is_mutual_match = False
        if has_liked:
            mutual_like = mongo.db.likes.find_one({
                'liker_id': ObjectId(user_id),
                'liked_id': ObjectId(current_user.id)
            })
            is_mutual_match = bool(mutual_like)
        
        return render_template('profile.html', 
                             user=user, 
                             has_liked=bool(has_liked), 
                             is_mutual_match=is_mutual_match)
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = int(request.form['age'])
            bio = request.form.get('bio', '')
            location = request.form.get('location', '')
            building_block = request.form.get('building_block', '')
            personality_type = request.form.get('personality_type', '')
            
            # Convert comma-separated strings to lists
            interests = [interest.strip() for interest in request.form.get('interests', '').split(',') if interest.strip()] if request.form.get('interests') else []
            study_habits = [habit.strip() for habit in request.form.get('study_habits', '').split(',') if habit.strip()] if request.form.get('study_habits') else []
            life_goals = [goal.strip() for goal in request.form.get('life_goals', '').split(',') if goal.strip()] if request.form.get('life_goals') else []
            
            # Update user profile in MongoDB Atlas
            mongo.db.users.update_one(
                {'_id': ObjectId(current_user.id)},
                {'$set': {
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'bio': bio,
                    'location': location,
                    'building_block': building_block,
                    'interests': interests,
                    'study_habits': study_habits,
                    'personality_type': personality_type,
                    'life_goals': life_goals
                }}
            )
            
            # Update current_user object
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.age = age
            current_user.bio = bio
            current_user.location = location
            current_user.building_block = building_block
            current_user.interests = interests
            current_user.study_habits = study_habits
            current_user.personality_type = personality_type
            current_user.life_goals = life_goals
            
            # Recalculate compatibility score
            current_user.calculate_compatibility_score()
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile', user_id=current_user.id))
        except Exception as e:
            flash(f'Profile update failed: {str(e)}', 'error')
    
    return render_template('edit_profile.html')

@app.route('/like_user/<user_id>', methods=['POST'])
@login_required
def like_user(user_id):
    try:
        if user_id == current_user.id:
            return jsonify({'success': False, 'message': 'You cannot like yourself!'})
        
        # Check if already liked
        existing_like = mongo.db.likes.find_one({
            'liker_id': ObjectId(current_user.id),
            'liked_id': ObjectId(user_id)
        })
        
        if existing_like:
            return jsonify({'success': False, 'message': 'You already liked this user!'})
        
        # Add like to MongoDB Atlas
        like_data = {
            'liker_id': ObjectId(current_user.id),
            'liked_id': ObjectId(user_id),
            'timestamp': datetime.now(timezone.utc)
        }
        mongo.db.likes.insert_one(like_data)
        
        # Create notification for the liked user
        notification_data = {
            'liker_id': ObjectId(current_user.id),
            'receiver_id': ObjectId(user_id),
            'message': f"{current_user.first_name} {current_user.last_name} liked your profile!",
            'timestamp': datetime.now(timezone.utc),
            'is_read': False
        }
        mongo.db.notifications.insert_one(notification_data)
        
        # Check for mutual match
        mutual_match = mongo.db.likes.find_one({
            'liker_id': ObjectId(user_id),
            'liked_id': ObjectId(current_user.id)
        })
        
        return jsonify({
            'success': True, 
            'message': 'Like sent successfully!' if not mutual_match else 'It\'s a match!',
            'is_match': bool(mutual_match)
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/matches')
@login_required
def matches():
    try:
        # Find mutual matches using MongoDB Atlas aggregation
        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'liker_id': ObjectId(current_user.id)},
                        {'liked_id': ObjectId(current_user.id)}
                    ]
                }
            },
            {
                '$group': {
                    '_id': {
                        '$cond': [
                            {'$eq': ['$liker_id', ObjectId(current_user.id)]},
                            '$liked_id',
                            '$liker_id'
                        ]
                    },
                    'likes_count': {'$sum': 1}
                }
            },
            {
                '$match': {'likes_count': {'$gte': 2}}
            }
        ]
        
        matches_result = list(mongo.db.likes.aggregate(pipeline))
        
        # Get matched users
        user_matches = []
        for match in matches_result:
            user_data = mongo.db.users.find_one({'_id': match['_id']})
            if user_data:
                user_matches.append(User(user_data))
        
        return render_template('matches.html', matches=user_matches)
    except Exception as e:
        flash(f'Error loading matches: {str(e)}', 'error')
        return render_template('matches.html', matches=[])

@app.route('/chat/<user_id>')
@login_required
def chat(user_id):
    try:
        other_user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not other_user_data:
            flash('User not found!', 'error')
            return redirect(url_for('matches'))
        
        other_user = User(other_user_data)
        
        # Check if they are matched
        is_matched = mongo.db.likes.find_one({
            '$or': [
                {
                    'liker_id': ObjectId(current_user.id),
                    'liked_id': ObjectId(user_id)
                },
                {
                    'liker_id': ObjectId(user_id),
                    'liked_id': ObjectId(current_user.id)
                }
            ]
        })
        
        if not is_matched:
            flash('You can only chat with matched users!', 'error')
            return redirect(url_for('matches'))
        
        # Get messages between these users
        chat_messages = list(mongo.db.messages.find({
            '$or': [
                {
                    'sender_id': ObjectId(current_user.id),
                    'receiver_id': ObjectId(user_id)
                },
                {
                    'sender_id': ObjectId(user_id),
                    'receiver_id': ObjectId(current_user.id)
                }
            ]
        }).sort('timestamp', 1))
        
        return render_template('chat.html', other_user=other_user, messages=chat_messages)
    except Exception as e:
        flash(f'Error loading chat: {str(e)}', 'error')
        return redirect(url_for('matches'))

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    try:
        receiver_id = request.form['receiver_id']
        content = request.form['content'].strip()
        
        if not content:
            return jsonify({'success': False, 'message': 'Message cannot be empty!'})
        
        # Check if they are matched
        is_matched = mongo.db.likes.find_one({
            '$or': [
                {
                    'liker_id': ObjectId(current_user.id),
                    'liked_id': ObjectId(receiver_id)
                },
                {
                    'liker_id': ObjectId(receiver_id),
                    'liked_id': ObjectId(current_user.id)
                }
            ]
        })
        
        if not is_matched:
            return jsonify({'success': False, 'message': 'You can only message matched users!'})
        
        # Create message in MongoDB Atlas
        message_data = {
            'sender_id': ObjectId(current_user.id),
            'receiver_id': ObjectId(receiver_id),
            'content': content,
            'timestamp': datetime.now(timezone.utc),
            'is_read': False
        }
        
        result = mongo.db.messages.insert_one(message_data)
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully!',
            'message_id': str(result.inserted_id),
            'timestamp': message_data['timestamp'].strftime('%H:%M')
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/get_messages/<user_id>')
@login_required
def get_messages(user_id):
    """Get messages between current user and another user for real-time updates"""
    try:
        # Check if they are matched
        is_matched = mongo.db.likes.find_one({
            '$or': [
                {
                    'liker_id': ObjectId(current_user.id),
                    'liked_id': ObjectId(user_id)
                },
                {
                    'liker_id': ObjectId(user_id),
                    'liked_id': ObjectId(current_user.id)
                }
            ]
        })
        
        if not is_matched:
            return jsonify({'success': False, 'message': 'You can only view messages with matched users!'})
        
        # Get messages between these users
        chat_messages = list(mongo.db.messages.find({
            '$or': [
                {
                    'sender_id': ObjectId(current_user.id),
                    'receiver_id': ObjectId(user_id)
                },
                {
                    'sender_id': ObjectId(user_id),
                    'receiver_id': ObjectId(current_user.id)
                }
            ]
        }).sort('timestamp', 1))
        
        # Convert ObjectId to string for JSON serialization
        for msg in chat_messages:
            msg['_id'] = str(msg['_id'])
            msg['sender_id'] = str(msg['sender_id'])
            msg['receiver_id'] = str(msg['receiver_id'])
            msg['timestamp'] = msg['timestamp'].strftime('%H:%M')
        
        return jsonify({
            'success': True,
            'messages': chat_messages
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/get_notifications')
@login_required
def get_notifications():
    try:
        # Get notifications for current user
        notifications = list(mongo.db.notifications.find({
            'receiver_id': ObjectId(current_user.id)
        }).sort('timestamp', -1).limit(10))
        
        # Format notifications
        formatted_notifications = []
        for notif in notifications:
            # Get liker's info
            liker_data = mongo.db.users.find_one({'_id': notif['liker_id']})
            if liker_data:
                formatted_notifications.append({
                    'id': str(notif['_id']),
                    'liker_id': str(notif['liker_id']),
                    'liker_name': f"{liker_data.get('first_name', '')} {liker_data.get('last_name', '')}",
                    'liker_picture': liker_data.get('profile_picture', ''),
                    'message': notif['message'],
                    'timestamp': notif['timestamp'].isoformat(),
                    'is_read': notif.get('is_read', False)
                })
        
        # Update unread count
        unread_count = mongo.db.notifications.count_documents({
            'receiver_id': ObjectId(current_user.id),
            'is_read': False
        })
        
        # Update current user object
        current_user.unread_notifications = unread_count
        
        return jsonify({
            'success': True,
            'notifications': formatted_notifications,
            'unread_count': unread_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/mark_notification_read/<notification_id>')
@login_required
def mark_notification_read(notification_id):
    try:
        # Mark notification as read
        mongo.db.notifications.update_one(
            {'_id': ObjectId(notification_id), 'receiver_id': ObjectId(current_user.id)},
            {'$set': {'is_read': True}}
        )
        
        # Update unread count
        unread_count = mongo.db.notifications.count_documents({
            'receiver_id': ObjectId(current_user.id),
            'is_read': False
        })
        
        # Update current user object
        current_user.unread_notifications = unread_count
        
        return jsonify({'success': True, 'unread_count': unread_count})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/delete_notification/<notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    try:
        # Delete notification
        result = mongo.db.notifications.delete_one({
            '_id': ObjectId(notification_id), 
            'receiver_id': ObjectId(current_user.id)
        })
        
        if result.deleted_count > 0:
            # Update unread count
            unread_count = mongo.db.notifications.count_documents({
                'receiver_id': ObjectId(current_user.id),
                'is_read': False
            })
            
            # Update current user object
            current_user.unread_notifications = unread_count
            
            return jsonify({'success': True, 'unread_count': unread_count})
        else:
            return jsonify({'success': False, 'message': 'Notification not found or unauthorized'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/mark_all_notifications_read')
@login_required
def mark_all_notifications_read():
    try:
        # Mark all notifications as read
        result = mongo.db.notifications.update_many(
            {'receiver_id': ObjectId(current_user.id), 'is_read': False},
            {'$set': {'is_read': True}}
        )
        
        # Update current user object
        current_user.unread_notifications = 0
        
        return jsonify({'success': True, 'updated_count': result.modified_count})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/clear_all_notifications')
@login_required
def clear_all_notifications():
    try:
        # Delete all notifications for the user
        result = mongo.db.notifications.delete_many({
            'receiver_id': ObjectId(current_user.id)
        })
        
        # Update current user object
        current_user.unread_notifications = 0
        
        return jsonify({'success': True, 'deleted_count': result.deleted_count})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
