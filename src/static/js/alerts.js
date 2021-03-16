const qAreaAlerts = document.querySelector(".area-alerts");

qAreaAlerts.addEventListener("click", function (e) {
  // Did we click the close button on an alert?
  if (e.target.matches(".msg-alert .btn-close")) {
    // Delete the clicked alert
    let alert = e.target.parentElement;
    alert.remove();

    // Delete the container once all messages are dismissed
    if (qAreaAlerts.childElementCount === 0) {
      qAreaAlerts.remove();
    }
  }
});
