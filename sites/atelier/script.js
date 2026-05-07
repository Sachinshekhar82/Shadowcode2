const dishes = [
  ["Citrus Ricotta Toast", "Whipped ricotta, honey, herbs, and charred sourdough."],
  ["Spiced Pear Tart", "Almond cream, warm pear slices, and brown butter glaze."],
  ["Smoked Tomato Omelet", "Soft eggs, greens, feta, and tomato jam."],
];

const dishName = document.getElementById("dishName");
const dishDesc = document.getElementById("dishDesc");
const reserveButton = document.getElementById("reserveButton");
let dishIndex = 0;

function rotateDish() {
  const [name, desc] = dishes[dishIndex];
  dishName.textContent = name;
  dishDesc.textContent = desc;
  dishIndex = (dishIndex + 1) % dishes.length;
}

setInterval(rotateDish, 3500);
rotateDish();

reserveButton.addEventListener("click", () => {
  reserveButton.textContent = "Booked for today";
});