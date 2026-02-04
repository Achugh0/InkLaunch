# Bulk User Import Feature

## Overview
The bulk user import feature allows administrators to import multiple users at once using a CSV file. This feature includes:

1. **Sample CSV Download**: A pre-populated sample file with 100 diverse international authors
2. **CSV Upload**: Web interface to upload and import users
3. **Validation**: Automatic validation of required fields and duplicate checking
4. **Error Reporting**: Detailed error messages for failed imports

## Accessing the Feature

1. Log in as an admin user
2. Navigate to **Admin Dashboard** → **Manage Users**
3. Click the **"Bulk Import"** button (green button next to "Create New User")

## CSV Format

The CSV file must have the following columns:

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| user_id | Yes | Unique username (no spaces) | priya_sharma |
| email | Yes | Valid email address | priya.sharma@inklaunch.in |
| Full_name | Yes | User's full name | Priya Sharma |
| password | Yes | User's password (will be encrypted) | SecurePass123 |
| role | No | User role (default: "User") | User or Admin |
| status | No | Account status (default: "active") | active, inactive, or suspended |
| BIO | No | User biography | "Award-winning novelist..." |

## Usage Instructions

### Method 1: Using the Web Interface

1. Navigate to `/admin/users/bulk-import`
2. Download the sample CSV file by clicking **"Download Sample CSV (100 Users)"**
3. Edit the CSV file with your user data (or use the sample as-is)
4. Upload the CSV file using the web form
5. Review the import results

### Method 2: Using the Command-Line Script

You can also import users directly using the Python script:

```bash
python import_sample_users.py [path_to_csv_file]
```

If no path is provided, it defaults to `sample_users.csv` in the root directory.

## Sample Users

The included `sample_users.csv` file contains 100 diverse users:
- Mix of Indian and international authors
- Various genres (romance, thriller, sci-fi, literary fiction, etc.)
- Different roles and backgrounds
- All users have the default password: `Ashna@1`

## Features

✅ **Duplicate Detection**: Skips users with existing usernames or emails  
✅ **Error Reporting**: Shows detailed errors for each failed import  
✅ **Bulk Processing**: Imports multiple users in one operation  
✅ **Password Encryption**: Automatically encrypts passwords using bcrypt  
✅ **Validation**: Validates all required fields before import  
✅ **Success Tracking**: Reports count of successful and failed imports  

## Error Handling

The system will skip users that:
- Have duplicate usernames
- Have duplicate email addresses
- Are missing required fields
- Have invalid data

All errors are reported at the end of the import process with row numbers for easy correction.

## Current Status

**Users in Database**: 97 (as of last import)

The sample CSV has been successfully imported with diverse international authors ready for testing and demonstration.

## Files

- `/sample_users.csv` - Sample CSV file with 100 users
- `/import_sample_users.py` - Command-line import script
- `/app/routes/admin.py` - Admin routes with bulk import endpoints
- `/app/templates/admin/bulk_import_users.html` - Web interface template

## API Endpoints

- `GET /admin/users/bulk-import` - Display upload form
- `POST /admin/users/bulk-import` - Process CSV upload
- `GET /admin/users/download-sample-csv` - Download sample CSV file
