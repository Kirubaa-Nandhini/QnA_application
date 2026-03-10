# Tasks: Refactor to Custom User Model

## Phase 1: Model & Settings Setup
- [x] Modify `accounts/models.py`:
  - [x] Import `AbstractUser`.
  - [x] Define `User(AbstractUser)` class.
  - [x] Add `bio` field.
- [x] Update `QnA_app/settings.py`:
  - [x] Configure `AUTH_USER_MODEL = 'accounts.User'`.
- [x] Remove `Profile` model from `accounts/models.py`.

## Phase 2: Database Reset & Migrations
- [x] Delete `db.sqlite3`.
- [x] Delete all migration files in `accounts/migrations/` (keep `__init__.py`).
- [x] Run `python manage.py makemigrations accounts`.
- [x] Run `python manage.py migrate`.

## Phase 3: Forms & Views Refactor
- [x] Update `accounts/forms.py`:
  - [x] Update `SignupForm` to use new `User`.
  - [x] Refactor `UserUpdateForm` and `ProfileUpdateForm` into a single `UserAccountForm`.
- [x] Update `accounts/views.py`:
  - [x] Update `SignupView` (remove `Profile.objects.create`).
  - [x] Update `ProfileView` (context mapping).
  - [x] Update `EditProfileView` (use new combined form).

## Phase 4: Templates & Cleanup
- [x] Update `accounts/templates/accounts/profile.html`:
  - [x] Update accessors (e.g., `user.bio` instead of `user_profile.bio`).
- [x] Update `accounts/templates/accounts/profile_edit.html`:
  - [x] Update form references.
- [x] Global search and replace for any `user.profile` or `User_profile` references.
