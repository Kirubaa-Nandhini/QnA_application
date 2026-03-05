# DESIGN - Search and Related Questions

## Overview
This design focuses on delivering efficient search functionality and relevant content discovery while maintaining the clean "Quora-inspired" aesthetic of the platform.

## Architecture

### 1. Keyword & Tag Search Logic
- **Endpoint**: `questions/` (Question List View)
- **Parameter**: `q` (e.g., `/questions/?q=django`)
- **Queryset filtering**:
  ```python
  from django.db.models import Q
  query = self.request.GET.get('q')
  if query:
      queryset = queryset.filter(
          Q(title__icontains=query) | 
          Q(description__icontains=query) |
          Q(tags__name__icontains=query)
      ).distinct()
  ```

### 2. Search UI
- **Navbar Integration**: Add a search input in the global navbar (in `base.html`).
- **Styling**: Rounded borders, subtle background, and a clear "Search" placeholder.

### 3. Related Questions Algorithm
- **Endpoint**: `questions/<id>/` (Question Detail View)
- **Logic**:
  ```python
  # Find questions with at least one shared tag
  related_questions = Question.objects.filter(
      tags__in=self.object.tags.all()
  ).exclude(id=self.object.id).annotate(
      num_shared_tags=models.Count('tags')
  ).order_by('-num_shared_tags', '-created_at')[:5]
  ```
- **Context**: Pass `related_questions` in `get_context_data`.

### 4. Detail Page Sidebar UI
- **Layout**: Change the `max-w-4xl` layout to a flex column/row on md+ screens.
- **Related List**: A simple, vertical list of links with truncated titles.
- **Visuals**: Use the existing design system (slate-400 for metadata, indigo-600 on hover).

## Key Components

### `QuestionListView`
- Responsible for combining `q`, `tag`, and `sort` parameters into a single optimized query.

### `QuestionDetailView`
- Responsible for calculating the "relevance" of other questions based on the tag intersection.

## Aesthetics
- Search bar: Quora-like, clean, light gray background.
- Sidebar: Minimalistic, no heavy borders, focus on text.
