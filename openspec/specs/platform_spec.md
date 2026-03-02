# Collaborative Q&A Platform — Master Specification

## 1. System Overview

The system is a collaborative Question and Answer platform built using Django.
It allows users to ask questions, post answers, comment, vote, and manage their content.

The platform supports public content visibility with authenticated user interaction.

---

## 2. Technology Constraints

- Framework: Django (Python)
- Database: SQLite
- Frontend: Django Templates + Tailwind CSS
- Authentication: Django Contrib Auth (Session-based)

---

## 3. User Roles

### Anonymous User
Can:
- View questions
- View answers
- View comments
- View user profiles

Cannot:
- Post content
- Vote
- Edit or delete content

### Authenticated User
Can:
- Create, edit, delete own questions
- Post answers
- Post comments
- Vote on content
- Accept an answer to their question
- Edit their profile

---

## 4. Core Entities

### 4.1 User
Uses Django's built-in User model.

### 4.2 Profile
- OneToOne with User
- Bio
- Profile picture (optional)
- Joined date

---

### 4.3 Question
Fields:
- Title
- Slug (unique)
- Description
- Author (FK → User)
- Tags (Many-to-Many)
- Created_at
- Updated_at

Rules:
- Only author can edit/delete
- Slug auto-generated from title
- Hard delete policy

---

### 4.4 Tag
Fields:
- Name
- Slug (unique)

---

### 4.5 Answer
Fields:
- Content
- Question (FK)
- Author (FK)
- Created_at
- Updated_at
- Is Accepted (Boolean)

Rules:
- Only one accepted answer per question
- Only question author can accept
- Hard delete policy

---

### 4.6 Comment
Fields:
- Content
- Author (FK)
- Created_at
- Generic relation to Question or Answer

Rules:
- Only author can edit/delete
- Hard delete policy

---

### 4.7 Vote
Fields:
- User (FK)
- Target Content (Generic relation)
- Vote Type (Upvote / Downvote)

Rules:
- One vote per user per content
- Toggle allowed
- Unique constraint enforced

---

## 5. Functional Requirements

### 5.1 Authentication
- User signup
- Login / Logout
- Password change
- Password reset via email

### 5.2 Question Management
- Create question
- Edit own question
- Delete own question
- View question list
- View question detail
- Filter by tag
- Sort by newest/oldest

### 5.3 Answer Management
- Post answer
- Edit own answer
- Delete own answer
- Accept answer

### 5.4 Comment System
- Add comment to question
- Add comment to answer
- Edit own comment
- Delete own comment

### 5.5 Voting System
- Upvote / Downvote questions
- Upvote / Downvote answers
- Upvote / Downvote comments
- Undo vote

### 5.6 User Profile
- Public profile page
- Display user's questions
- Display user's answers
- Display joined date

---

## 6. Security Rules

- All write operations require authentication.
- Edit/Delete operations require content ownership validation.
- Accept answer requires question ownership validation.
- CSRF protection enabled for all forms.

---

## 7. Deletion Policy

All deletions are hard deletes.

---

## 8. Performance Guidelines

- Use select_related and prefetch_related
- Add DB index on:
  - Slug
  - Foreign keys
  - Created_at
- Pagination required for listing pages

---

## 9. Out of Scope

- Bookmarking
- Notifications
- Soft delete
- Social login
- Full-text PostgreSQL search