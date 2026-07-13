# Frontend Assessment — Movie Search

Welcome, and thanks for taking the time. This is a ~45-minute live coding
exercise. We care far more about how you think, structure code, and work with
React than about a pixel-perfect result. Please **think out loud** and ask
questions whenever you like.

## The task

Turn the provided design into a working React app: a page that searches movies
using the TMDB API and shows the results as a grid of cards.

The design lives in Figma — see [`design/README.md`](design/README.md) for the
link and a description of everything on the page.

## Setup (≈2 minutes)

The `starter/` folder is a ready-to-run Vite + React + Tailwind project. The
toolchain, colour theme, fonts, icons, and a loading `Spinner` are already done
so you can spend your time on React.

1. Your interviewer will give you a **TMDB API token** at the start.
2. In `starter/`, copy `.env.example` to `.env` and paste the token into
   `VITE_TMDB_API_KEY`.
3. Install and run:
   ```bash
   cd starter
   npm install
   npm run dev
   ```
4. Open the printed local URL. You should see the hero heading and an empty
   "Search" section — that's the starting point.

## What we've left for you

Look for `// TODO` markers:

- `src/api/tmdb.js` — implement `searchMovies()`.
- `src/components/Search.jsx` — the search input.
- `src/components/MovieCard.jsx` — a single result card.
- `src/App.jsx` — state, data fetching, and rendering the grid.

You're free to change structure, add files, or add a dependency if you want one.

## What to build

**Core (aim to finish these):**

1. **Hero + search bar** matching the design — the heading (with *Movies* in the
   purple accent colour) and the search input with its icon and placeholder. (The
   decorative poster banner is optional — no image asset is provided for it.)
2. **Fetch movies from TMDB.** When the box is empty, show popular movies so the
   page is never empty. When there's a search term, show matching movies.
3. **Render the results grid** of cards — each showing the poster, title, and
   star rating.
4. **Loading & error states** — show the provided `<Spinner />` while a request
   is in flight, and a readable message if a request fails or returns nothing.

**If you have time:**

5. When typing in the search box, avoid sending a request on every keystroke —
   optimize the search input handling.
6. **Pagination** — the prev / `page / total` / next control at the bottom.

## TMDB reference

- Getting started: https://developer.themoviedb.org/docs/getting-started
- Search: `GET /3/search/movie?query=...&page=...`
- Popular / discover: `GET /3/discover/movie?sort_by=popularity.desc&page=...`
- Poster image: `https://image.tmdb.org/t/p/w500<poster_path>`
- Auth is already wired: requests send `Authorization: Bearer <your token>`.

## How we'll evaluate

- **React fundamentals** — components, props/state, effects, list keys,
  conditional rendering.
- **Code structure** — clear components, sensible state placement, readable
  naming.
- **API & async handling** — correct fetching, loading/error handling.
- **Design fidelity** — a reasonable match to the screenshot (not pixel-perfect).

Have fun — a clean, working core beats a half-finished attempt at everything.
