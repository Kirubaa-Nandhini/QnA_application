# Design: Add Authentication System

## Architecture
The system will leverage Django's default authentication framework, customized with Tailwind CSS for a premium user experience.

### 1. Data Models
- **User**: Standard `django.contrib.auth.models.User`.
- **Profile**: A One-to-One extension of the User model.
  - Fields: `user` (FK), `bio` (Text), `profile_picture` (Image), `joined_date` (DateTime).

### 2. Authentication & Profile Flow
- **Signup**: Custom `SignupView` using a `UserCreationForm` subclass. Automatic login after successful signup.
- **Login/Logout**: Built-in Django views (`LoginView`, `LogoutView`) with custom templates.
- **Profile View**: A dedicated view to display user info (Name, Email) and statistics.
  - Stats: Calculated using `Count` on the user's related `questions` and `answers`.
- **Password Change**: Implement `PasswordChangeView` to allow users to update their credentials securely.

### 3. UI / UX
- **Base Layout**: `base.html` with a sticky glassmorphism navigation bar.
- **Conditional Nav**: For anonymous users, show "Login/Signup". For authenticated users, show "Profile" (with the user's name) and "Logout".
- **Profile Layout**: A clean, dashboard-like view with distinct cards for personal info and activity stats.
- **Tailwind Integration**: All forms and pages styled with a modern, high-contrast palette.

### 4. Integration
- New `accounts` app to house all authentication logic.
- Project-level `urls.py` inclusion of `accounts.urls`.
- Global settings for `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL`.
