"""Migrate local /uploads images to Cloudinary and update MongoDB URLs."""
import os
import sys
from pathlib import Path

import cloudinary
import cloudinary.uploader
from pymongo import MongoClient


def require_env(name):
    value = os.getenv(name)
    if not value:
        print(f"❌ Missing env var: {name}")
        sys.exit(1)
    return value


def upload_file(local_path, folder):
    result = cloudinary.uploader.upload(
        str(local_path),
        folder=folder,
        resource_type="auto",
        quality="auto",
        fetch_format="auto",
    )
    return result.get("secure_url")


def migrate_collection(db, collection_name, field_name, folder, upload_root):
    print(f"\n== {collection_name}.{field_name} -> {folder} ==")
    updated = 0
    missing = 0

    cursor = db[collection_name].find({field_name: {"$regex": r"^(\/)?uploads\/"}})
    for doc in cursor:
        url = doc.get(field_name, "")
        filename = os.path.basename(url)
        local_path = upload_root / filename

        if not local_path.exists():
            print(f"⚠ Missing file: {local_path}")
            missing += 1
            continue

        try:
            new_url = upload_file(local_path, folder)
            if new_url:
                db[collection_name].update_one(
                    {"_id": doc["_id"]},
                    {"$set": {field_name: new_url}},
                )
                print(f"✓ {filename} -> {new_url}")
                updated += 1
            else:
                print(f"❌ Upload failed: {filename}")
        except Exception as exc:
            print(f"❌ Upload error for {filename}: {exc}")

    print(f"Updated: {updated}, Missing: {missing}")


def main():
    cloud_name = require_env("CLOUDINARY_CLOUD_NAME")
    api_key = require_env("CLOUDINARY_API_KEY")
    api_secret = require_env("CLOUDINARY_API_SECRET")
    mongo_uri = require_env("MONGODB_URI")

    upload_folder = os.getenv("UPLOAD_FOLDER", "uploads")
    upload_root = Path(upload_folder).expanduser().resolve()

    if not upload_root.exists():
        print(f"❌ Uploads folder not found: {upload_root}")
        sys.exit(1)

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )

    client = MongoClient(mongo_uri)
    db = client.inklaunch

    migrate_collection(db, "books", "cover_image_url", "book-covers", upload_root)
    migrate_collection(db, "users", "profile_image_url", "profile-images", upload_root)
    migrate_collection(db, "users", "banner_image_url", "banner-images", upload_root)

    client.close()
    print("\n✅ Migration complete.")


if __name__ == "__main__":
    main()
