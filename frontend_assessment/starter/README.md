# Movie Search — Starter

A pre-configured Vite + React + Tailwind CSS v4 project.

## Run

```bash
cp .env.example .env      # then paste your TMDB token into VITE_TMDB_API_KEY
npm install
npm run dev
```

Open the local URL Vite prints.

## Layout

- `src/api/tmdb.js` — TMDB helper (auth wired; `searchMovies()` to implement).
- `src/components/Search.jsx` — search input shell (provided; controlled via props).
- `src/components/MovieCard.jsx` — result card (to create).
- `src/components/Spinner.jsx` — loading spinner (provided).
- `src/App.jsx` — hero + search already rendered; wire fetch + grid (TODOs).
- `src/index.css` — Tailwind import + design theme tokens (provided).

Tailwind v4 is configured via the `@tailwindcss/vite` plugin and the `@theme`
block in `src/index.css` — there is no `tailwind.config.js`.
