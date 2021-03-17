// Detect if the user wants a dark theme
const themeDark = window.matchMedia("(prefers-color-scheme: dark)");

function applyLightTheme() {
  document.body.classList.remove("dark");
}

function applyDarkTheme() {
  document.body.classList.add("dark");
}

/**
 * Used to set the dark theme on page load, if needed.
 */
if (themeDark.matches) {
  applyDarkTheme();
}

// Listen for theme changes
themeDark.addEventListener("change", function (e) {
  (e.matches ? applyDarkTheme : applyLightTheme)();
});
