const cards = document.querySelectorAll(".card");

cards.forEach((card) => {
  card.addEventListener("pointermove", (event) => {
    const bounds = card.getBoundingClientRect();
    const x = ((event.clientX - bounds.left) / bounds.width) * 100;
    const y = ((event.clientY - bounds.top) / bounds.height) * 100;
    card.style.background = `radial-gradient(circle at ${x}% ${y}%, rgba(255,255,255,0.12), rgba(10,19,33,0.72) 42%)`;
  });

  card.addEventListener("pointerleave", () => {
    card.style.background = "rgba(10, 19, 33, 0.72)";
  });
});