/* POLITIK RIUH — token launch site, Phase 1
   Single progressive-enhancement behaviour: the mobile navigation toggle.
   Without JavaScript the full navigation stays visible (see styles.css).
   Keyboard: the toggle is a native <button>, so Enter/Space activate it.
   Escape closes an open menu and returns focus to the toggle.
   No tracking, no network requests, no wallet code. */
(function () {
  document.documentElement.classList.add("js");

  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;

  function setOpen(open) {
    if (open) {
      nav.classList.add("is-open");
    } else {
      nav.classList.remove("is-open");
    }
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.textContent = open ? "Tutup menu" : "Menu";
  }

  toggle.addEventListener("click", function () {
    setOpen(!nav.classList.contains("is-open"));
  });

  // Escape closes an open menu and returns focus to the toggle, so keyboard
  // users are never left stranded inside a menu that just closed.
  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape" || !nav.classList.contains("is-open")) return;
    setOpen(false);
    toggle.focus();
  });
})();
