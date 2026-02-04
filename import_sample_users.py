"""Import sample users from CSV file."""
import csv
import sys
from datetime import datetime
from app import create_app, mongo, bcrypt

def import_users_from_csv(csv_file_path):
    """Import users from CSV file."""
    app = create_app()
    
    with app.app_context():
        success_count = 0
        error_count = 0
        errors = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                
                for row_num, row in enumerate(csv_reader, start=2):
                    try:
                        # Check if user already exists
                        existing_user = mongo.db.users.find_one({'username': row['user_id']})
                        if existing_user:
                            errors.append(f"Row {row_num}: Username '{row['user_id']}' already exists")
                            error_count += 1
                            continue
                        
                        existing_email = mongo.db.users.find_one({'email': row['email']})
                        if existing_email:
                            errors.append(f"Row {row_num}: Email '{row['email']}' already exists")
                            error_count += 1
                            continue
                        
                        # Create user
                        user_data = {
                            'username': row['user_id'],
                            'email': row['email'],
                            'full_name': row['Full_name'],
                            'password_hash': bcrypt.generate_password_hash(row['password']).decode('utf-8'),
                            'role': row.get('role', 'user').lower(),
                            'status': row.get('status', 'active').lower(),
                            'is_active': row.get('status', 'active').lower() == 'active',
                            'bio': row.get('BIO', ''),
                            'created_at': datetime.utcnow(),
                            'updated_at': datetime.utcnow(),
                            'profile_image': None,
                            'social_links': {},
                            'preferences': {},
                            'badges': []
                        }
                        
                        mongo.db.users.insert_one(user_data)
                        success_count += 1
                        print(f"✓ Created user: {row['user_id']} ({row['Full_name']})")
                        
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                        error_count += 1
                        print(f"✗ Error at row {row_num}: {str(e)}")
        
        except FileNotFoundError:
            print(f"Error: File '{csv_file_path}' not found")
            return
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return
        
        # Print summary
        print("\n" + "="*60)
        print("IMPORT SUMMARY")
        print("="*60)
        print(f"Successfully imported: {success_count} users")
        print(f"Failed to import: {error_count} users")
        
        if errors:
            print("\nErrors:")
            for error in errors[:20]:  # Show first 20 errors
                print(f"  - {error}")
            if len(errors) > 20:
                print(f"  ... and {len(errors) - 20} more errors")

if __name__ == '__main__':
    csv_file = 'sample_users.csv'
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    
    print(f"Importing users from: {csv_file}")
    import_users_from_csv(csv_file)
