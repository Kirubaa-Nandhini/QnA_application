import django.db.models.deletion
from django.db import migrations, models
import django.utils.timezone

def move_profile_data(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        # Check if accounts_profile table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts_profile';")
        if cursor.fetchone():
            print("\nMigrating data from accounts_profile to auth_user...")
            # Copy bio and joined_date to auth_user for matching user IDs
            cursor.execute("""
                UPDATE auth_user 
                SET bio = COALESCE((SELECT bio FROM accounts_profile WHERE accounts_profile.user_id = auth_user.id), ''),
                    joined_date = COALESCE((SELECT joined_date FROM accounts_profile WHERE accounts_profile.user_id = auth_user.id), auth_user.date_joined)
                WHERE EXISTS (SELECT 1 FROM accounts_profile WHERE accounts_profile.user_id = auth_user.id)
            """)
            # Drop the old profile table
            cursor.execute("DROP TABLE accounts_profile")
            print("Successfully migrated profile data and dropped accounts_profile table.")

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='joined_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.RunPython(move_profile_data, reverse_code=migrations.RunPython.noop),
    ]
