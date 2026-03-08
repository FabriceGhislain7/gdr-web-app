(function footerEnhancements() {
  function updateTime() {
    const now = new Date();
    const locale = document.body?.dataset?.timeLocale || "en-US";
    const timeString = now.toLocaleTimeString(locale, {
      hour: "2-digit",
      minute: "2-digit"
    });

    const timeElement = document.getElementById("current-time");
    if (timeElement) {
      timeElement.textContent = timeString;
    }
  }

  updateTime();
  setInterval(updateTime, 60000);

  document.querySelector(".footer h5")?.addEventListener("click", function onTitleClick() {
    window.scrollTo({ top: 0, behavior: "smooth" });
    this.style.transform = "scale(1.1)";
    setTimeout(() => {
      this.style.transform = "scale(1)";
    }, 200);
  });

  document.querySelectorAll(".social-links a").forEach((link) => {
    link.addEventListener("click", (event) => {
      const sparkle = document.createElement("div");
      sparkle.textContent = "\u2728";
      sparkle.style.position = "absolute";
      sparkle.style.left = `${event.pageX}px`;
      sparkle.style.top = `${event.pageY}px`;
      sparkle.style.pointerEvents = "none";
      sparkle.style.fontSize = "20px";
      sparkle.style.zIndex = "9999";
      sparkle.style.animation = "sparkleFloat 1s ease-out forwards";

      document.body.appendChild(sparkle);
      setTimeout(() => sparkle.remove(), 1000);
    });
  });

  const style = document.createElement("style");
  style.textContent = `
    @keyframes sparkleFloat {
      0% { opacity: 1; transform: translateY(0) scale(1); }
      100% { opacity: 0; transform: translateY(-30px) scale(1.5); }
    }
  `;
  document.head.appendChild(style);
})();
