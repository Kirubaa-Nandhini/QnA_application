# Design: Community Engagement System

## Overview
The system will provide interactive layers (voting and comments) for both Questions and Answers. By using polymorphic-style models (`ContentType`), we ensure a consistent experience across different content types while avoiding code duplication.

## Data Models

### `Vote`
- `user`: ForeignKey to `User`.
- `content_type`: ForeignKey to `ContentType`.
- `object_id`: PositiveIntegerField.
- `content_object`: GenericForeignKey.
- `value`: IntegerField (1 for upvote, -1 for downvote).
- `created_at`: DateTimeField.
*Uniqueness Constraint*: `user`, `content_type`, and `object_id` must be unique together to allow only one vote per item per user.

### `Comment`
- `user`: ForeignKey to `User`.
- `content_type`: ForeignKey to `ContentType`.
- `object_id`: PositiveIntegerField.
- `content_object`: GenericForeignKey.
- `content`: TextField.
- `parent`: ForeignKey to `self` (for nested/threaded replies, nullable).
- `created_at`: DateTimeField.

## User Interface

### Voting Component
- Upvote/Downvote buttons next to questions and answers.
- Display current score (Upvotes - Downvotes).
- Active state for the user's current vote.
- Asynchronous updates using Fetch API to avoid page reloads.

### Threaded Comments
- Interactive "Comment" button to reveal a form.
- Display comments below each question/answer.
- "Reply" button on each comment to facilitate threading.
- Indented layout for replies.

### Share Component
- Simple "Share" button.
- "Copy Link" functionality that copies the question's direct URL to the clipboard.
- Visual feedback (e.g., a "Copied!" tooltip or transient alert) when the link is successfully copied.

## Backend Implementation
- **Generic Views**: Create a unified `VoteToggleView` and `CommentCreateView`.
- **Managers**: Add a custom manager to `Question` and `Answer` to easily retrieve vote counts and comment counts.
- **Signals**: Potentially use signals to update counters if performance becomes an issue, though aggregation is preferred initially.

## Security & Permissions
- Authentication required for voting and commenting.
- Rate limiting on voting to prevent abuse.
- Validation to prevent users from voting multiple times or voting on their own content.
