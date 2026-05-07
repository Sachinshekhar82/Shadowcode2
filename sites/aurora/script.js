const pace = document.getElementById("pace");
const statusValue = document.getElementById("statusValue");
const statusLabel = document.getElementById("statusLabel");
const ring = document.querySelector(".ring");

function updatePulse(value) {
  const percent = Math.round((value / 2.4) * 100);
  statusValue.textContent = `${percent}%`;
  statusLabel.textContent = percent >= 80 ? "Stable" : percent >= 55 ? "Monitoring" : "Surging";
  ring.style.animationDuration = `${10 / value}s`;
}

pace.addEventListener("input", (event) => updatePulse(Number(event.target.value)));
updatePulse(Number(pace.value));