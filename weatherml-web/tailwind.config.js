/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"DM Sans"', "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "ui-monospace", "monospace"],
      },
      colors: {
        surface: {
          DEFAULT: "#0c1222",
          card: "#141c2c",
          elevated: "#1e2a3f",
          muted: "#94a3b8",
        },
        accent: {
          DEFAULT: "#38bdf8",
          glow: "#7dd3fc",
        },
      },
      boxShadow: {
        card: "0 4px 24px -4px rgba(0, 0, 0, 0.45), inset 0 1px 0 0 rgba(255,255,255,0.04)",
        glow: "0 0 40px -10px rgba(56, 189, 248, 0.35)",
      },
    },
  },
  plugins: [],
};
