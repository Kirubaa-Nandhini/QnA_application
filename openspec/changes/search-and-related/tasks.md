# TASKS - Search and Related Questions

## Phase 1: Search Implementation
- [x] Add a search input and form to `templates/base.html` in the navbar.
- [x] Update `QuestionListView` in `questions/views.py` to filter the queryset by the `q` parameter using `Q` objects across title, description, and tag names.
- [x] Ensure the search term is preserved in pagination links in `question_list.html`.
- [x] Test that search combined with tags and sorting works correctly.

## Phase 2: Related Questions
- [x] Update `QuestionDetailView` in `questions/views.py` to fetch related questions sharing at least one tag.
- [x] Implement ranking for related questions by the count of shared tags.
- [x] Update `question_detail.html` layout to include a sidebar for "Related Questions".
- [x] Style the related questions list as clean, minimalist links.

## Phase 3: UX & Polish
- [x] Add a "Clear Search" or "No results found" message to the list page.
- [x] Optimize queries to avoid unnecessary joins when calculating related questions.
- [x] Verify responsive behavior on mobile (search bar vs. sidebar).
