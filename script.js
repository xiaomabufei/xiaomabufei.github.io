document.getElementById("year").textContent = new Date().getFullYear();

const groups = Array.from(document.querySelectorAll(".project-group"));
const canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

groups.forEach((group) => {
  const summary = group.querySelector("summary");
  let enterTimer;
  let leaveTimer;
  let pinned = false;
  let hovering = false;

  const syncMedia = (expanded) => {
    group.querySelectorAll("video[data-src]").forEach((video) => {
      if (expanded) {
        if (!video.src) {
          video.src = video.dataset.src;
          video.load();
        }
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    });
  };

  const expand = (value) => {
    group.open = value;
    summary.setAttribute("aria-expanded", String(value));
    syncMedia(value);
  };

  summary.setAttribute("aria-expanded", String(group.open));
  syncMedia(group.open);
  summary.addEventListener("click", (event) => {
    event.preventDefault();
    clearTimeout(enterTimer);
    clearTimeout(leaveTimer);
    pinned = !pinned;
    group.classList.toggle("is-pinned", pinned);
    expand(pinned || hovering);
  });

  if (!canHover) return;
  group.addEventListener("mouseenter", () => {
    hovering = true;
    clearTimeout(leaveTimer);
    enterTimer = setTimeout(() => expand(true), 180);
  });
  group.addEventListener("mouseleave", () => {
    hovering = false;
    clearTimeout(enterTimer);
    leaveTimer = setTimeout(() => {
      if (!pinned) expand(false);
    }, 450);
  });
});
