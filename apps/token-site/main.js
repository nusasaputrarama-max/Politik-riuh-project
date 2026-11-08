/* POLITIK RIUH — token launch site, Phase 1
   Single progressive-enhancement behaviour: the mobile navigation toggle.
   Without JavaScript the full navigation stays visible (see styles.css).
   No tracking, no network requests, no wallet code. */
(function () {
  document.documentElement.classList.add("js");

  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;

  toggle.addEventListener("click", function () {
    var open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.textContent = open ? "Close menu" : "Menu";
  });
})();
