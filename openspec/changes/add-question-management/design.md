# Design: Add Question Management

## Architecture
The system will be housed in a new `questions` app, following Django's MTV (Model-Template-View) pattern.

### 1. Data Models
- **Tag**: 
  - `name`: CharField (unique)
  - `slug`: SlugField (unique)
- **Question**:
  - `title`: CharField
  - `slug`: SlugField (unique)
  - `description`: TextField (Markdown supported)
  - `author`: FK to `User`
  - `tags`: M2M to `Tag`
  - `created_at` / `updated_at`: DateTimeFields

### 2. Views & Logic
- **List View**: Paginated list with sorting (Newest/Oldest) and tag filtering.
- **Detail View**: Displays the question description (rendered via Markdown).
- **Create/Update View**: 
  - Uses a custom `QuestionForm`.
  - Automatic slug generation and author assignment.

### 3. UI / UX
- **List Page**: Modern cards with tag badges and author info.
- **Form Page**: Clean, single-column layout with real-time feedback.
- **Markdown Support**: Use a library like `markdown2` or `django-markdown-deux` for rendering.

### 4. Permissions
- `LoginRequiredMixin` for all write operations.
- `UserPassesTestMixin` to ensure only authors can edit or delete their questions.
