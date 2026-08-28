// Provided for you — the loading indicator is not part of what's being assessed.
// Render <Spinner /> while a request is in flight.
export default function Spinner() {
  return (
    <div className="flex justify-center py-10" role="status" aria-label="Loading">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-white/20 border-t-accent" />
    </div>
  );
}
