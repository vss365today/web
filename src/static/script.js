(function() {
  "use strict";

  // @src https://medium.com/free-code-camp/how-to-detect-a-users-preferred-color-scheme-in-javascript-ec8ee514f1ef
  const DARK = "(prefers-color-scheme: dark)";
  const LIGHT = "(prefers-color-scheme: light)";
  const NO_PREF = "(prefers-color-scheme: no-preference)";

  // We don't have the api we need to detect the state
  // although considering the caniuse.com stats,
  // this shold not be an issue at all
  if (!window.matchMedia) {
    return false;
  }

  // Detect the possible states
  // @src https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme
  const inDarkMode = window.matchMedia(DARK).matches;
  const inLightMode = window.matchMedia(LIGHT).matches;
  const noPrefMode = window.matchMedia(NO_PREF).matches;

  // TODO Decide if I should default to dark theme
  // ui.systemUsesDarkTheme
  // if (inDarkMode || (noPrefMode === false)) {

  // Only enable the dark theme if the browser setting is on
  if (inDarkMode) {
    document.body.classList.add("dark");
  }
}());
