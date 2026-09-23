// TMDB API helper.
//
// The base URL and auth header are set up for you. Your job is to implement
// searchMovies() so it calls the right TMDB endpoints and returns the data
// App.jsx needs.
//
// Docs: https://developer.themoviedb.org/docs/getting-started
// Useful endpoints:
//   GET /search/movie?query=...&page=...        (when there is a search term)
//   GET /discover/movie?sort_by=popularity.desc (default list, empty search)

const API_BASE_URL = "https://api.themoviedb.org/3";

const API_OPTIONS = {
  method: "GET",
  headers: {
    accept: "application/json",
    Authorization: `Bearer ${import.meta.env.VITE_TMDB_API_KEY}`,
  },
};

// Build a full poster URL from a TMDB poster_path (may be null).
export const posterUrl = (path) =>
  path ? `https://image.tmdb.org/t/p/w500${path}` : null;

/**
 * Fetch movies from TMDB.
 * @param {string} query - the search term (empty string => popular movies)
 * @param {number} page  - 1-based page number
 * @returns {Promise<{ results: Array, page: number, total_pages: number }>}
 *
 * TODO: implement this.
 *  - choose the endpoint based on whether `query` is empty
 *  - fetch with API_OPTIONS
 *  - throw a helpful error if the response is not ok
 *  - return the parsed JSON
 */
export async function searchMovies(query, page = 1) {
  // TODO: your code here
  throw new Error("searchMovies is not implemented yet");
}
