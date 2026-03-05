# Tasks: Community Engagement Implementation

## 1. Foundation & Models
- [ ] Create `Comment` model in `questions/models.py` using `GenericForeignKey`.
- [ ] Create `Vote` model in `questions/models.py` using `GenericForeignKey`.
- [ ] Implement `get_score` and `get_comments` helper methods on `Question` and `Answer` models.
- [ ] Run migrations to update the database schema.

## 2. API & Logic
- [ ] Implement `VoteToggleView` to handle up/down voting via AJAX.
- [ ] Implement `CommentCreateView` to handle new comments and nested replies.
- [ ] Create serializers or JSON responses for the async voting system.
- [ ] Add URL patterns for voting and commenting.

## 3. Templates & UI Components
- [ ] Build a reusable `voting_controls.html` partial.
- [ ] Build a `comment_section.html` partial with support for nesting.
- [ ] Update `question_detail.html` to integrate voting and comments for the main **Question**.
- [ ] Update `question_detail.html` to integrate voting and comments for **each individual Answer**.
- [ ] Update `question_list.html` to display vote and comment counts for questions.
- [ ] Add a "Share" button with Copy Link functionality to `question_detail.html`.

## 4. Interaction & Polishing
- [ ] Add JavaScript logic to handle AJAX voting updates.
- [ ] Implement "Show/Hide Comments" toggle functionality.
- [ ] Add "Copy Link" to clipboard functionality with a "Copied" alert.
- [ ] Style all new elements with Tailwind CSS for a premium feel.

## 5. Testing & Validation
- [ ] Verify that users cannot vote twice on the same item.
- [ ] Test nested commenting up to at least 2 levels.
- [ ] Ensure only authenticated users can vote/comment.
- [ ] Check responsive design on mobile and tablet views.
