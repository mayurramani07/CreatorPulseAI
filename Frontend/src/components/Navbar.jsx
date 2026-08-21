import { useState } from "react";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="fixed inset-x-0 top-0 z-50 border-b border-white/[0.06] bg-[#08090d]/80 backdrop-blur-xl">

      <div className="mx-auto flex h-14 w-full max-w-7xl items-center justify-between px-5 sm:px-6 lg:px-8">

        {/* Brand */}

        <a
          href="#home"
          className="text-[20px] font-semibold tracking-tight text-white sm:text-[22px]"
          onClick={() => setMenuOpen(false)}
        >
          CreatorPulse
          <span className="text-violet-400">AI</span>
        </a>


        {/* Desktop Navigation */}

        <div className="hidden items-center gap-8 md:flex">

          <a
            href="#home"
            className="text-sm font-medium text-zinc-400 transition-colors duration-200 hover:text-white"
          >
            Home
          </a>

          <a
            href="#engineering"
            className="text-sm font-medium text-zinc-400 transition-colors duration-200 hover:text-white"
          >
            Engineering
          </a>

          <a
            href="#about"
            className="text-sm font-medium text-zinc-400 transition-colors duration-200 hover:text-white"
          >
            About
          </a>

        </div>


        {/* Mobile Menu Button */}

        <button
          type="button"
          onClick={() => setMenuOpen(!menuOpen)}
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/[0.08] bg-white/[0.03] text-zinc-300 transition hover:border-white/[0.15] hover:bg-white/[0.06] hover:text-white md:hidden"
          aria-label="Toggle navigation menu"
          aria-expanded={menuOpen}
        >
          {menuOpen ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.8}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.8}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          )}
        </button>

      </div>


      {/* Mobile Navigation */}

      {menuOpen && (
        <div className="border-t border-white/[0.06] bg-[#08090d]/95 px-5 py-4 backdrop-blur-xl md:hidden">

          <div className="mx-auto flex max-w-7xl flex-col gap-1">

            <a
              href="#home"
              onClick={() => setMenuOpen(false)}
              className="rounded-lg px-3 py-3 text-sm font-medium text-zinc-400 transition-colors hover:bg-white/[0.04] hover:text-white"
            >
              Home
            </a>

            <a
              href="#engineering"
              onClick={() => setMenuOpen(false)}
              className="rounded-lg px-3 py-3 text-sm font-medium text-zinc-400 transition-colors hover:bg-white/[0.04] hover:text-white"
            >
              Engineering
            </a>

            <a
              href="#about"
              onClick={() => setMenuOpen(false)}
              className="rounded-lg px-3 py-3 text-sm font-medium text-zinc-400 transition-colors hover:bg-white/[0.04] hover:text-white"
            >
              About
            </a>

          </div>

        </div>
      )}

    </nav>
  );
}

export default Navbar;