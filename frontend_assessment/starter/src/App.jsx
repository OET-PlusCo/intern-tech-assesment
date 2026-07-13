import Spinner from "./components/Spinner.jsx";
import { searchMovies } from "./api/tmdb.js";

export default function App() {

  // TODO: fetch movies from TMDB.
  //  - load popular movies on first render
  //  - re-fetch when the search term changes

  return (
    <main className="hero-pattern min-h-screen">
      <div className="mx-auto max-w-5xl px-5 py-12">
        <section className="mt-10">
          <h2 className="text-2xl font-bold text-white">Movies</h2>
          <Spinner  />
        </section>
      </div>
    </main>
  );
}
