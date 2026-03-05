# Design: Implement Answer Management System

## Architecture
The answer management system will be integrated into the existing `questions` app.

### 1. Data Models
- **Answer**:
  - `question`: FK to `Question` (related_name='answers')
  - `author`: FK to `User` (related_name='answers')
  - `content`: TextField (Markdown supported)
  - `created_at`: DateTimeField (auto_now_add=True)
  - `updated_at`: DateTimeField (auto_now=True)

### 2. Views & Logic
- **Inline Submission**: Handle answer creation either via a separate `CreateView` or by processing POST data in `QuestionDetailView`.
- **Edit/Delete**: Class-based views (`AnswerUpdateView`, `AnswerDeleteView`) with permission checks.
- **Display**: Use the `related_name` in templates to iterate over all answers for a given question.

### 3. UI / UX
- **Submission Form**: A simple, clean textarea with a "Post Answer" button, visible only to logged-in users.
- **Answer List**: Modern cards for each answer, showing the author (and their initial), timestamp, and content.
- **Stats**: Update the User Profile view to include the actual count of answers provided by the user.

### 4. Permissions
- `LoginRequiredMixin` for all answer submission and modification.
- `UserPassesTestMixin` to ensure only the author of an answer can edit or delete it.
