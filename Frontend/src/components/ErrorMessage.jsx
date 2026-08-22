function ErrorMessage({ message }) {
  if (!message) {
    return null;
  }

  return (
    <div className="mx-auto mt-6 w-full max-w-3xl">
      <div className="flex items-start gap-3 rounded-xl border border-red-400/10 bg-red-500/[0.04] px-4 py-4">

        <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg border border-red-400/10 bg-red-500/[0.06] text-red-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.8}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 9v3.75m0 3.75h.008M10.29 3.86l-7.04 12.2A1.5 1.5 0 0 0 4.55 18.3h14.9a1.5 1.5 0 0 0 1.3-2.24l-7.04-12.2a1.5 1.5 0 0 0-2.6 0Z"
            />
          </svg>
        </div>

        <div>
          <p className="text-sm font-medium text-red-300">
            Analysis failed
          </p>

          <p className="mt-1 text-xs leading-5 text-red-300/60">
            {message}
          </p>
        </div>

      </div>
    </div>
  );
}

export default ErrorMessage;