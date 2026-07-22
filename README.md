# RapidDev Calendar Dashboard

Static HTML/Tailwind mockup of a personal calendar & scheduling dashboard.

## Pages

- `code.html` — main dashboard (profile, meeting stats, upcoming meetings, meeting balance chart). Serves as the site's home page (`/`).
- `calendar.html` — full month calendar view with a "New Event" creation modal and per-event details popup.

Both pages share the same design tokens (Tailwind CDN config, color palette, typography, corner-smoothing "squircle" treatment) so they behave as one connected app rather than two isolated files.

## Tech

- Static HTML, no build step.
- [Tailwind CSS](https://tailwindcss.com) via the CDN JIT script (`?plugins=forms,container-queries`).
- [Material Symbols](https://fonts.google.com/icons) for iconography.
- [Manrope](https://fonts.google.com/specimen/Manrope) for typography.
- [figma-squircle](https://github.com/figma/figma-squircle) (loaded from jsDelivr) for iOS-style continuous corner smoothing.

No dependencies to install and nothing to build — the pages are self-contained and fetch their few external resources (fonts, icons, the squircle script) directly from CDNs at load time.

## Running locally

Any static file server works, for example:

```bash
npx serve .
# or
python3 -m http.server 8000
```

Then open `http://localhost:PORT/code.html` (dashboard) or `http://localhost:PORT/calendar.html` (calendar).

## Deploying to Vercel

This repo needs no build command or output directory — it's deployed as-is as a static site.

1. Push this repository to GitHub.
2. In Vercel, "Add New Project" → import the GitHub repo.
3. Framework preset: **Other** (no build step). Leave build/output settings blank — `vercel.json` handles the rest.
4. Deploy.

`vercel.json` in this repo maps the root URL (`/`) to `code.html`, so the dashboard loads at the site's home page; `calendar.html` is reachable at `/calendar` (clean URLs are enabled).

## Design reference

`DESIGN.md` contains the original design-system brief (colors, type scale, spacing, elevation) this mockup was built from. Note that the shipped palette (RapidDev brand red/navy) has since diverged from the doc's original cyan color scheme — the doc is kept for historical/process reference, not as the current source of truth.
