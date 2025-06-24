const form = document.getElementById("matchForm");
const result = document.getElementById("resultado");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const porcentaje = Math.floor(Math.random() * 101);

  let mensaje = "";
  let emoji = "";
  if (porcentaje >= 90) {
    mensaje = "¡Almas gemelas!";
    emoji = "💘💍💑";
  } else if (porcentaje >= 70) {
    mensaje = "Alta compatibilidad";
    emoji = "❤️💫";
  } else if (porcentaje >= 50) {
    mensaje = "Conexión posible";
    emoji = "💞✨";
  } else if (porcentaje >= 30) {
    mensaje = "Flechazo dudoso";
    emoji = "💔🤷";
  } else {
    mensaje = "Por lo menos se conocen perfectamente";
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
