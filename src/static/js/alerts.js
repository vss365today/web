(function () {
  "use strict";

  const qAreaAlerts = document.querySelector(".area-alerts");

  qAreaAlerts.addEventListener("click", function (e) {
    if (e.target.matches(".msg-alert .btn-close")) {
      let thisNotif = e.target.parentElement;
      thisNotif.classList.add("hidden");

      // Perform a fade out transition before removing the notification
      thisNotif.addEventListener(
        "transitionend",
        function (e) {
          if (e.propertyName === "opacity") {
            e.target.remove();

            // Delete the container once all messages are dismissed
            if (qAreaAlerts.childElementCount === 0) {
              qAreaAlerts.remove();
            }
          }
        },
        { once: true }
      );
    }
  });
})();
