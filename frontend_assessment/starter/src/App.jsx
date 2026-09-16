import { useState } from "react";
import Spinner from "./components/Spinner.jsx";
import Search from "./components/Search.jsx";
import { searchMovies } from "./api/tmdb.js";

export default function App() {

  // TODO: fetch movies from TMDB.
  //  - load popular movies on first render
  //  - re-fetch when the search term changes
  //  - track loading / error / results
  //  - render a grid of movies cards

  return (
    <main className="hero-pattern min-h-screen">
      <div className="mx-auto max-w-5xl px-5 py-12">
        <header className="mt-6 text-center">
          <h1 className="text-4xl font-bold leading-tight text-white sm:text-5xl">
            Find <span className="text-accent">Movies</span> You&apos;ll Love
            <br />
            Without the Hassle
          </h1>
          <Search />
        </header>

        <section className="mt-14">
          <h2 className="text-2xl font-bold text-white">Search</h2>
          {/* TODO: replace Spinner with loading / error / empty / movie grid */}
          <Spinner />
        </section>
      </div>
    </main>
  );
}
