(function() {
  "use strict";
  const STORAGE_KEY = "is-dark-theme";
  const userTheme = window.localStorage.getItem(STORAGE_KEY);

  function isDarkTheme() {
    return document.body.classList.contains("dark");
  }

  function applyDarkTheme() {
    document.body.classList.toggle("dark", !isDarkTheme());
    window.localStorage.setItem(STORAGE_KEY, isDarkTheme().toString());
  }

  // Determine the theme to use initially by checking `prefers-color-scheme`,
  // defaulting to the light theme, but then checking if the user has manually set a theme
  // and using it instead
  let wantsDarkTheme = matchMedia("(prefers-color-scheme: dark)").matches;
  if (userTheme) {
    wantsDarkTheme = (userTheme === "true");
  }

  // Set or remove the `dark` class on page load
  document.body.classList.toggle("dark", wantsDarkTheme);
}());
