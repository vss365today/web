(function () {
  "use strict";

  const qFlashMessagesContainer = document.querySelector(".msg-flash-area");

  qFlashMessagesContainer.addEventListener("click", function (e) {
    if (e.target.matches(".msg-flash .btn-close")) {
      let thisNotif = e.target.parentElement;
      thisNotif.classList.add("hidden");

      // Perform a fade out transition before removing the notification
      thisNotif.addEventListener(
        "transitionend",
        function (e) {
          if (e.propertyName === "opacity") {
            e.target.remove();

            // Delete the container once all messages are dismissed
            if (qFlashMessagesContainer.childElementCount === 0) {
              qFlashMessagesContainer.remove();
            }
          }
        },
        { once: true }
      );
    }
  });
})();
