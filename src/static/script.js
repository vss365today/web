(function() {
  "use strict";
  function isDarkTheme() {
    return !!(document.cookie.split(';').filter((item) => item.includes('is-dark-theme=true')).length);
  }

  /**
   * @param {boolean} apply
   */
  function applyDarkTheme(apply) {
    document.body.classList.toggle("dark", apply);
    let cookie = `is-dark-theme=${apply};path=/;domain=${window.location.hostname};max-age=31536000;samesite=strict`;

    // Secure the cookie when in production
    if (window.location.hostname === "vss365today.com") {
      cookie = `__Secure-${cookie};secure`;
    }
    document.cookie = cookie;
  }

  // Allow the user to toggle between the themes
  document.querySelector("nav.primary #btn-theme").addEventListener("click", function() {
    applyDarkTheme(!isDarkTheme());
  });
}());
