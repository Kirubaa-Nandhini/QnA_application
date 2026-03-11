import django.db.models.deletion
from django.db import migrations, models
import django.utils.timezone

def move_profile_data(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        # Check if bio column exists in auth_user
        cursor.execute("PRAGMA table_info(auth_user);")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Only add if they are missing
        if 'bio' not in columns:
            print("Adding bio column to auth_user table...")
            cursor.execute("ALTER TABLE auth_user ADD COLUMN bio TEXT DEFAULT '' NOT NULL;")
        
        if 'joined_date' not in columns:
            print("Adding joined_date column to auth_user table...")
            # SQLite specific: can't easily add with current time as default without complexity, using now()
            cursor.execute(f"ALTER TABLE auth_user ADD COLUMN joined_date DATETIME DEFAULT '{django.utils.timezone.now().isoformat()}' NOT NULL;")

        # Check if accounts_profile table exists to migrate data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts_profile';")
        if cursor.fetchone():
            print("\nMigrating data from accounts_profile to auth_user...")
            cursor.execute("""
                UPDATE auth_user 
                SET bio = COALESCE((SELECT bio FROM accounts_profile WHERE accounts_profile.user_id = auth_user.id), ''),
                    joined_date = COALESCE((SELECT joined_date FROM accounts_profile WHERE accounts_profile.user_id = auth_user.id), auth_user.date_joined)
                WHERE EXISTS (SELECT 1 FROM accounts_profile WHERE accounts_profile.user_id = auth_user.id)
            """)
            print("Successfully migrated profile data.")

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_add_user_fields_and_data'), # Depends on the version Django thinks is applied
    ]

    operations = [
        migrations.RunPython(move_profile_data, reverse_code=migrations.RunPython.noop),
    ]
