import searchIcon from "../assets/search.svg";

/**
 * Search input shell — UI is provided.
 */
export default function Search() {
  return (
    <div className="mx-auto mt-8 flex w-full max-w-xl items-center gap-3 bg-white/5 px-4 py-3">
      <img src={searchIcon} alt="" className="size-5 shrink-0" aria-hidden="true" />
      <input
        type="text"
        placeholder="Search through 300+ movies online"
        className="w-full text-base placeholder:text-gray-100"
        aria-label="Search movies"
      />
    </div>
  );
}
