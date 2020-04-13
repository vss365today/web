"use strict";

const qFlashMessagesContainer = document.querySelector(".msg-flash-area");

qFlashMessagesContainer.addEventListener("click", (e) => {
  if (e.target.matches(".msg-flash .btn-close")) {
    e.target.parentElement.remove();
  }
});