# DESIGN - System-wide Dark Mode

## Overview
This design implements a robust dark mode using Tailwind CSS classes. We will use the 'class' strategy, where a `.dark` class is applied to the `<html>` element to trigger dark variants.

## Architecture

### 1. Tailwind Integration
- Since we are using CDN Tailwind for now, we need to ensure the configuration allows class-based dark mode.
- Update `tailwind.config` (if available) or the CDN runtime configuration.

### 2. Prevention of FOUC (Flash of Unstyled Content)
- Place an inline script in the `<head>` of `base.html` before any body content:
  ```javascript
  if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  ```

### 3. Theme Toggle Component
- **Location**: Navbar, next to the search bar or profile links.
- **Interaction**:
  - Clicking toggles the `localStorage` value between `'light'` and `'dark'`.
  - Also toggles the `.dark` class on `document.documentElement`.
- **Icon**: Use a Sun (light mode) and Moon (dark mode) SVG toggle.

### 4. Color Palette Mapping

| Element | Light Mode | Dark Mode |
| :--- | :--- | :--- |
| **Body BG** | `bg-slate-50` | `dark:bg-slate-950` |
| **Cards** | `bg-white` | `dark:bg-slate-900` |
| **Borders** | `border-slate-200` | `dark:border-slate-800` |
| **Heading Text** | `text-slate-900` | `dark:text-white` |
| **Body Text** | `text-slate-600` | `dark:text-slate-400` |
| **Navbar** | `bg-white/80` | `dark:bg-slate-950/80` |
| **Hover State** | `hover:bg-slate-100` | `dark:hover:bg-slate-800` |

### 5. Markdown Adjustments
- The `prose` class needs the `dark:prose-invert` utility to automatically adjust typography colors for dark backgrounds.

## Implementation Steps
1. Modify `base.html` to include the FOUC prevention script and the toggle button.
2. Create `static/js/theme_toggle.js` for the runtime logic.
3. Systematically update all templates (`question_list.html`, `question_detail.html`, etc.) with `dark:` utility classes.
