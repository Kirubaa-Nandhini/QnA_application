# Design: Refactor to Custom User Model

## Architecture
We will replace the dual-model structure (`User` + `Profile`) with a single custom `User` model. This model will inherit from `AbstractUser`, making it compatible with all built-in Django authentication features while allowing us to attach custom fields directly to the user object.

### 1. Data Models Refactor
- **User**: Custom model inheriting from `AbstractUser`.
  - Additional Fields:
    - `bio`: `TextField(max_length=500, blank=True)` (Moved from `Profile`).
  - Mapping:
    - `joined_date` from `Profile` will be retired in favor of the built-in `date_joined` on `AbstractUser`.
- **Profile**: This model will be **removed**.

### 2. Form & View Adjustments
- **Forms**:
  - `SignupForm`: Update to use the new `User` model.
  - `ProfileUpdateForm`: Instead of needing two forms, a single `ModelForm` on the custom `User` model will handle all fields (username, first_name, last_name, email, bio).
- **Views**:
  - `ProfileView`: Update context to access `bio` directly from `user` instead of `user_profile`.
  - `EditProfileView`: Simplify logic to use a single form. `transaction.atomic` will still be good practice but less critical for cross-model consistency.
  - `SignupView`: Remove the manual `Profile.objects.create` step.

### 3. Migration Strategy
Since this is a development environment, the strategy will be:
1. Delete existing migrations in `accounts/migrations/` (except `__init__.py`).
2. Delete the `db.sqlite3` database to ensure a clean slate (or use a migration that handles data transfer if preferred, but resetting is safer for a clean custom user model implementation).
3. Create initial migrations.
4. Update `AUTH_USER_MODEL` in `settings.py`.

### 4. Code References
All instances of `user.profile` or `Profile` imports will need to be updated:
- `accounts/views.py`: Access `request.user.bio`.
- `accounts/templates/accounts/profile.html`: Access `user.bio`.
- `questions/models.py`: Ensure `ForeignKey` to `settings.AUTH_USER_MODEL`.
