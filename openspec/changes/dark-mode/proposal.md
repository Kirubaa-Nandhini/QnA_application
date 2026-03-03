# PROPOSAL - System-wide Dark Mode

## Problem
Currently, the QnA application only supports a light theme. This can cause eye strain for users in low-light environments and lacks the modern "Dark Mode" aesthetic that many users expect. Providing a toggle allows users to customize their experience and improves accessibility.

## User Persona
- **Night Owls**: Users who browse the platform late at night or in dark rooms.
- **Power Users**: Users who prefer dark interfaces for aesthetic reasons and reduced glare.
- **Accessibility Seekers**: Users with light sensitivity who find high-contrast dark themes easier to read.

## Goals
- Implement a system-wide "Dark Mode" using Tailwind CSS's `dark:` variant.
- Add a theme toggle button in the navbar for easy switching.
- Persist the user's theme preference using `localStorage` so it remains consistent across sessions.
- Ensure all UI components (cards, buttons, inputs, typography) are optimized for both themes.

## Solution
1. **Tailwind Configuration**: Enable the `darkMode: 'class'` strategy in Tailwind.
2. **Theme Toggle**: Add a sun/moon icon toggle in the `base.html` navbar.
3. **Persistance Logic**: Add a small inline script in `<head>` to prevent "flash of unstyled content" (FOUC) by checking `localStorage` early.
4. **Style Audit**: Apply `dark:` classes to all core templates and partials.

## Success Criteria
- A user can toggle between light and dark themes instantly.
- The chosen theme is remembered after a page refresh or browser restart.
- No "white flash" occurs when loading a page in dark mode.
- All text remains readable and all components maintain their premium look in dark mode.
