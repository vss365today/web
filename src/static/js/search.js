function findParentElement(element, selector) {
  "use strict";
  // The desired element was not found on the page
  if (element === null) {
    return null;
  }

  // We found the desired element
  if (element.matches(selector)) {
    return element;

    // Keep searching for the element
  } else {
    return findParentElement(element.parentElement, selector);
  }
}

// Create the ability to toggle among search tabs
const qSearchTabs = document.querySelector(".form-search-tabs");
qSearchTabs.addEventListener("click", function (e) {
  // Find the clicked tab
  let ele = findParentElement(e.target, ".form-search-tabs .tab:not(.active)");
  if (ele) {
    // Switch the active tab
    document
      .querySelector(".form-search-tabs .tab.active")
      .classList.remove("active");
    ele.classList.add("active");

    // Show the desired search form
    let searchType = ele.classList[1];
    document.querySelector(".form-search.active").classList.remove("active");
    document
      .querySelector(".form-search." + searchType)
      .classList.add("active");
  }
});

// Create a prettier select element
tail.select(document.querySelector("#input-search-host"), {
  search: true,
  placeholder: "ArthurUnkTweets",
});
