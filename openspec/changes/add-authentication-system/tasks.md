# Tasks: Add Authentication System

## Phase 1: Setup
- [ ] Create `accounts` Django app.
- [ ] Add `accounts` to `INSTALLED_APPS`.
- [ ] Configure `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` to `'home'`.

## Phase 2: Data & Logic
- [ ] Implement `Profile` model and migrations.
- [ ] Create `SignupForm` (email required).
- [ ] Implement `SignupView` with automatic login.
- [ ] Implement custom `logout_user` view (POST method).
- [ ] Implement `ProfileView` with question/answer count statistics.
- [ ] Implement `PasswordChangeManualView` (or utilize built-in `PasswordChangeView`).

## Phase 3: Templates & UI
- [ ] Update `base.html` with authenticated navigation links (Home, Profile, Logout).
- [ ] Create `login.html` template with Tailwind styling.
- [ ] Create `signup.html` template with formatted password instructions.
- [ ] Create `profile.html` template with user info and stats.
- [ ] Create `password_change.html` and `password_change_done.html` templates.
- [ ] Create a clean `home.html` hero section.

## Phase 4: Routing
- [ ] Include `accounts.urls` in project `urls.py`.
- [ ] Map signup, login, logout, profile, and password change routes.
