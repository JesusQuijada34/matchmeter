const form = document.getElementById("matchForm");
const result = document.getElementById("resultado");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const porcentaje = Math.floor(Math.random() * 101);

  let mensaje = "";
  let emoji = "";
  if (porcentaje >= 90) {
    mensaje = "¡Almas gemelas!";
    emoji = "💍💑";
  } else if (porcentaje >= 80) {
    mensaje = "Flechados!";
    emoji = "🎯🌀";
  } else if (porcentaje >= 70) {
    mensaje = "Un alma cerca tuyo";
    emoji = "👻🌊";
  } else if (porcentaje >= 60) {
    mensaje = "Pareja perfecta";
    emoji = "👥💕";
  } else if (porcentaje >= 50) {
    mensaje = "Mejores amigos";
    emoji = "❤️💫";
  } else if (porcentaje >= 40) {
    mensaje = "Son amigos";
    emoji = "💞✨";
  } else if (porcentaje >= 30) {
    mensaje = "Es algo infiel";
    emoji = "👎🧐";
  } else if (porcentaje >= 20) {
    mensaje = "Aquella persona tiene pareja";
    emoji = "🐺🔮";
  } else if (porcentaje >= 10) {
    mensaje = "Encontré infidelidad";
    emoji = "💔🤷";
  } else {
    mensaje = "Nada que ver";
    emoji = "😅🚫";
  }

  const frases = [
    "El amor verdadero empieza con la verdad.",
    "A veces, los opuestos no solo se atraen… se equilibran.",
    "El corazón sabe cosas que la mente no entiende.",
    "Hoy es un buen día para decir lo que sientes 💬",
    "El futuro es incierto, pero el cariño sincero siempre brilla.",
    "Si te hace reír, ya ganó puntos 😄",
    "La compatibilidad es el arte de aceptarse sin intentar cambiar al otro.",
    "Escucha más allá de las palabras 💗",
    "Un gesto vale más que mil promesas.",
    "A veces, el destino solo necesita un empujoncito..."
  ];

  const fraseAleatoria = frases[Math.floor(Math.random() * frases.length)];

  result.innerHTML = `
    <strong>Resultado:</strong> ${porcentaje}% - ${mensaje} ${emoji}<br/><br/>
    <em>🧠 Consejo:</em> "${fraseAleatoria}"
  `;
});
