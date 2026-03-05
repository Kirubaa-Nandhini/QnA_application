# PROPOSAL - Search and Related Questions

## Problem
Currently, users have no easy way to find specific questions among the growing list of content. They have to scroll through pages or rely on basic tag filtering. Additionally, when viewing a question, there's no way to discover similar content, which leads to lower user retention and engagement.

## User Persona
- **Active Searchers**: Users who know what they are looking for and want to find it quickly via keywords.
- **Casual Browsers**: Users who find a question interesting and want to explore other questions about the same specific topic.

## Goals
- Provide a robust keyword search (icontains) that covers the title, description, and associated tags of questions.
- Display a "Related Questions" sidebar on the detail page to surface similar content based on shared tags.

## Solution
1. **Keyword & Tag Search**:
   - Add a search input to the navbar or the question list page.
   - Update `QuestionListView` to filter the queryset using `icontains` on title/description and matching on tag names.
2. **Related Questions**:
   - Update `QuestionDetailView` to identify questions sharing tags with the current one.
   - Rank related questions by number of shared tags for better relevance.
   - Update the UI to show a clean list of these related links.

## Success Criteria
- A user can type a keyword or tag name and see relevant questions.
- The question detail page displays 3-5 high-relevance related questions.
