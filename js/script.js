const form = document.getElementById("matchForm");
const result = document.getElementById("resultado");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const love = ["💘 98% Compatibles", "💞 85% Compatibles", "❤️ 72% Compatibles", "💔 45% Compatibilidad", "🚫 0%... Mejor lazo unible"];
  const random = love[Math.floor(Math.random() * love.length)];

  result.textContent = `Resultado: ${random}`;
  result.style.color = "#ffffff";
});
