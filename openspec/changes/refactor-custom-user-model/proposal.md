# Proposal: Refactor User and Profile into Custom User Model

## Problem
Currently, the application uses Django's default `User` model and a separate `Profile` model connected via a `OneToOneField`. This split requires extra queries (O(1) join but still extra work), complex dual-form handling in views (as seen in the recent profile edit implementation), and manual signal handling or explicit creation of profiles on signup.

Specifically:
- Accessing bio requires `request.user.profile.bio`.
- Updating both User and Profile requires atomic transactions and multiple form instances.
- The `AbstractUser` approach is the recommended best practice for modern Django projects from the start.

## Solution
Refactor the architecture to use a custom `User` model inheriting from `AbstractUser`.
- Merge `Profile.bio` into the custom `User` model.
- Map `Profile.joined_date` to the built-in `date_joined` field of `AbstractUser`.
- Remove the `Profile` model entirely.
- Update `settings.py` with `AUTH_USER_MODEL = 'accounts.User'`.

This will:
- Simplify views and forms.
- Improve database performance (fewer joins).
- Provide a cleaner API: `request.user.bio` instead of `request.user.profile.bio`.

## Non-goals
- Changing the authentication backends.
- Adding social auth.
- Major UI changes (the forms and profile pages will look the same but work differently under the hood).
