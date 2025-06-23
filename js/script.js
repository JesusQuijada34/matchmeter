document.addEventListener('DOMContentLoaded', function() {
    const checkBtn = document.getElementById('checkBtn');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('resultContainer');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    const compatibilityValue = document.getElementById('compatibilityValue');
    const strengths = document.getElementById('strengths');
    const advice = document.getElementById('advice');
    const heartFill = document.getElementById('heartFill');
    const percentage = document.getElementById('percentage');
    const closeBtn = document.getElementById('closeBtn');

    // Frases para los resultados
    const strengthsList = [
        "Comunicación excelente",
        "Química increíble",
        "Valores compartidos",
        "Paciencia mutua",
        "Aventureros juntos",
        "Apoyo incondicional",
        "Risas constantes",
        "Confianza total",
        "Creatividad compartida",
        "Pasión intensa"
    ];

    const adviceList = [
        "Sigan comunicándose abiertamente",
        "Reserven tiempo para citas románticas",
        "Aprendan a resolver conflictos juntos",
        "Mantengan la chispa con sorpresas",
        "Cultiven sus intereses compartidos",
        "Respeten siempre el espacio del otro",
        "No dejen de ser ustedes mismos",
        "Planifiquen un futuro juntos",
        "Celebren sus diferencias",
        "Nunca dejen de cortejar al otro"
    ];

    const messages = {
        high: [
            "¡Es una conexión increíble!",
            "¡Están hechos el uno para el otro!",
            "¡El amor verdadero existe!",
            "¡Una pareja perfecta!"
        ],
        medium: [
            "¡Tienen mucho potencial!",
            "¡Con trabajo pueden ser grandiosos!",
            "¡Una buena base para construir!",
            "¡Vale la pena intentarlo!"
        ],
        low: [
            "Podría ser un reto interesante...",
            "Las diferencias pueden complementarse",
            "Todo requiere esfuerzo",
            "El amor puede superar obstáculos"
        ]
    };

    checkBtn.addEventListener('click', checkCompatibility);
    closeBtn.addEventListener('click', closeResult);

    function checkCompatibility() {
        const person1 = document.getElementById('person1').value.trim();
        const person2 = document.getElementById('person2').value.trim();

        if (!person1 || !person2) {
            alert("Por favor ingresa ambos nombres");
            return;
        }

        // Mostrar loader
        showLoader();

        // Resetear corazón
        heartFill.style.height = '0%';
        percentage.textContent = '0%';

        // Simular tiempo de carga (3 segundos)
        setTimeout(() => {
            // Ocultar loader
            hideLoader();

            // Calcular porcentaje "aleatorio" (pero basado en los nombres para consistencia)
            const compatPercent = calculateCompatibility(person1, person2);
            
            // Animar el corazón
            animateHeart(compatPercent);

            // Mostrar resultados
            showResult(compatPercent);
        }, 3000);
    }

    function calculateCompatibility(name1, name2) {
        // Hacer el cálculo "aleatorio" pero consistente para los mismos nombres
        const combinedNames = (name1 + name2).toLowerCase().replace(/s/g, '');
        let hash = 0;
        
        for (let i = 0; i < combinedNames.length; i++) {
            hash = combinedNames.charCodeAt(i) + ((hash << 5) - hash);
        }

        // Asegurar que esté entre 20% y 99%
        const percent = Math.abs(hash) % 80 + 20;
        return percent > 99 ? 99 : percent;
    }

    function animateHeart(percent) {
        let currentPercent = 0;
        const increment = percent / 50;
        
        const interval = setInterval(() => {
            currentPercent += increment;
            if (currentPercent >= percent) {
                currentPercent = percent;
                clearInterval(interval);
            }
            
            heartFill.style.height = ${currentPercent}%;
            percentage.textContent = ${Math.round(currentPercent)}%;
        }, 20);
    }

    function showResult(percent) {
        // Seleccionar mensajes según el porcentaje
        let messageGroup;
        if (percent >= 80) messageGroup = messages.high;
        else if (percent >= 50) messageGroup = messages.medium;
        else messageGroup = messages.low;
        
        const randomMessage = messageGroup[Math.floor(Math.random() * messageGroup.length)];
        const randomStrength = strengthsList[Math.floor(Math.random() * strengthsList.length)];
        const randomAdvice = adviceList[Math.floor(Math.random() * adviceList.length)];

        // Actualizar el DOM
        resultTitle.textContent = ${randomMessage};
        resultMessage.textContent = ${document.getElementById('person1').value} y ${document.getElementById('person2').value};
        compatibilityValue.textContent = ${percent}%;
        strengths.textContent = randomStrength;
        advice.textContent = randomAdvice;

        // Mostrar el resultado
        resultContainer.classList.add('show');
    }

    function closeResult() {
        resultContainer.classList.remove('show');
        // Resetear el formulario
        document.getElementById('person1').value = '';
        document.getElementById('person2').value = '';
    }

    function showLoader() {
        loader.classList.remove('hidden');
        loader.style.display = 'block';
    }

    function hideLoader() {
        loader.classList.add('hidden');
        setTimeout(() => {
            loader.style.display = 'none';
        }, 300);
    }
});
