const pace = document.getElementById("pace");
const focusValue = document.getElementById("focusValue");
const orb = document.querySelector(".orb");

function updateFocus(value) {
  const focus = Math.round((value / 10) * 100);
  focusValue.textContent = `${focus}%`;
  orb.style.animationDuration = `${5 - value * 0.25}s`;
}

pace.addEventListener("input", (event) => updateFocus(Number(event.target.value)));
updateFocus(Number(pace.value));