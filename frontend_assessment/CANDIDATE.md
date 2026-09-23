# Frontend Assessment — Movie Search

Welcome, and thanks for taking the time. This is a ~20-minute live coding
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
toolchain, colour theme, fonts, icons, hero heading, search input shell, and a
loading `Spinner` are already done so you can spend your time on React + data.

1. Your interviewer will give you a **TMDB API token** at the start.
2. In `starter/`, copy `.env.example` to `.env` and paste the token into
   `VITE_TMDB_API_KEY`.
3. Install and run:
   ```bash
   cd starter
   npm install
   npm run dev
   ```
4. Open the printed local URL. You should see the hero heading and search bar —
   that's the starting point.

## What we've left for you

Look for `// TODO` markers:

- `src/api/tmdb.js` — implement `searchMovies()`.
- `src/App.jsx` — state, data fetching, and rendering the grid.

`Search.jsx` is already wired as a controlled input — keep using it.

You're free to change structure, add files, or add a dependency if you want one.

## What to build

**Aim to finish these (~20 minutes):**

1. **Fetch movies from TMDB.** When the box is empty, show popular movies so the
   page is never empty. When there's a search term, show matching movies.
2. **Render the results grid** of cards — each showing the poster, title, and
   star rating (use the provided `star.svg`). Handle a missing poster with a
   simple "Poster Not Available" placeholder.
3. **Loading & error states** — show the provided `<Spinner />` while a request
   is in flight, and a readable message if a request fails or returns nothing.

The hero and search bar UI are already in place — you only need to connect data.

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
- **Design fidelity** — a reasonable match to the card layout (not pixel-perfect).

Have fun — a clean, working core beats a half-finished attempt at extras.
