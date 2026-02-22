export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#020617",
        panel: "#020617",
        glass: "rgba(255,255,255,0.05)",
        accent: "#22d3ee",
        danger: "#ef4444",
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(34,211,238,.25), 0 20px 40px rgba(0,0,0,.7)",
      },
      backdropBlur: {
        xl: "20px",
      },
    },
  },
  plugins: [],
};