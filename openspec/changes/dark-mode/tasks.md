# TASKS - System-wide Dark Mode

## Phase 1: Foundation
- [x] Configure Tailwind for class-based dark mode in `base.html`.
- [x] Add the FOUC prevention inline script to the `<head>` of `base.html`.
- [x] Create `static/js/theme_toggle.js` to handle the toggle click events and `localStorage` updates.

## Phase 2: UI Implementation
- [x] Add the theme toggle button (Sun/Moon icons) to the navbar in `base.html`.
- [x] Implement `dark:` classes for the global `<body>`, `<nav>`, and `<main>` containers.
- [x] Update `question_list.html` with dark mode support for cards, tags, and text.
- [x] Update `question_detail.html` with dark mode support, including `prose-invert` for Markdown content.
- [x] Apply dark mode styles to the sidebar filters and "Related Questions" sidebar.

## Phase 3: Fine-tuning
- [x] Ensure form inputs and textareas in `question_form.html` and `answer_form` are styled for dark mode.
- [x] Audit the comment sections and voting pills for dark mode visibility.
- [x] Verify that the "Markdown Editor" toolbar and interactions work correctly in dark mode.
- [x] Test the transition smoothness (using `transition-colors`).
