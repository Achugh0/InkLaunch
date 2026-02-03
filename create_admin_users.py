"""Create admin users with specified passwords."""
import sys
from app import create_app, bcrypt, mongo

app = create_app()

with app.app_context():
    # Admin users to create
    admin_users = [
        {
            'email': 'ashchugh@gmail.com',
            'password': 'Ashna@2000!',
            'full_name': 'Admin User 1',
            'bio': 'Platform Administrator',
            'role': 'admin'
        },
        {
            'email': 'achugh@hotmail.com',
            'password': 'Ashna@2000!',
            'full_name': 'Admin User 2',
            'bio': 'Platform Administrator',
            'role': 'admin'
        }
    ]
    
    for admin_data in admin_users:
        # Check if user exists
        existing_user = mongo.db.users.find_one({'email': admin_data['email'].lower()})
        
        if existing_user:
            # Update existing user
            password_hash = bcrypt.generate_password_hash(admin_data['password']).decode('utf-8')
            mongo.db.users.update_one(
                {'email': admin_data['email'].lower()},
                {'$set': {
                    'password_hash': password_hash,
                    'role': 'admin',
                    'is_active': True
                }}
            )
            print(f"✓ Updated user: {admin_data['email']}")
        else:
            # Create new user
            from datetime import datetime
            password_hash = bcrypt.generate_password_hash(admin_data['password']).decode('utf-8')
            
            user_doc = {
                'email': admin_data['email'].lower(),
                'password_hash': password_hash,
                'full_name': admin_data['full_name'],
                'bio': admin_data['bio'],
                'profile_image_url': '',
                'role': admin_data['role'],
                'is_active': True,
                'total_nominations': 0,
                'total_wins': 0,
                'author_of_month_count': 0,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            result = mongo.db.users.insert_one(user_doc)
            print(f"✓ Created admin user: {admin_data['email']} (ID: {result.inserted_id})")
    
    print("\n✓ Admin users setup complete!")
    print("  - ashchugh@gmail.com")
    print("  - achugh@hotmail.com")
    print("  - Password: Ashna@2000!")
    print(f"\nAccess admin console at: http://localhost:5000/admin/dashboard")
