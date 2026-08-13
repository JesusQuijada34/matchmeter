# Matchmeter

**Identidad del paquete:** `influent.matchmeter.v1.0-26.08-21.56`
**Autor:** `JesusQuijada34`
**Plataforma:** `AlphaCube`
**Descripción:** Estructura reparada por MoonFix

## Estructura PackageMaker 3.2.7

Este repositorio fue normalizado mediante **MoonFix**, usando la estructura de PackageMaker 3.2.7. El paquete público debe conservar `details.xml`, `version.res`, `autorun`, `autorun.bat`, `.storedetail`, `updater.py`, `config/settings.json`, los marcadores `.container` y los archivos de documentación correspondientes. El publisher oficial es `influent` y la versión pública no contiene sufijo de plataforma.

## Instalación y ejecución

Instala las dependencias declaradas en `lib/requirements.txt` cuando exista y ejecuta el entrypoint real del proyecto. En Linux, los comandos privilegiados son específicos de Danenone y no deben trasladarse a Windows. En proyectos AlphaCube, la validación Windows debe realizarse con el `buildthis` oficial de PackageMaker.

## Validación

La fuente debe pasar compilación sintáctica, pruebas funcionales disponibles, comprobación de identidad XML, protección contra traversal en ZIP y llamadas seguras a subprocess. Los artefactos `.iflapp` deben ser generados por PackageMaker; los paquetes Debian deben usar el nombre canónico `influent.matchmeter.v1.0-26.08-21.56_ARCH.deb`.

## Release

El tag y el título del release deben ser exactamente `v1.0-26.08-21.56`. Los assets deben usar el nombre canónico del paquete y una extensión objetiva. No se permite publicar un release AlphaCube que contenga únicamente el build Linux.

## Referencia original

# **MatchMeter 💖 - Medidor de Compatibilidad Amorosa**

**MatchMeter** es una aplicación divertida y ligera que calcula un porcentaje recreativo de compatibilidad entre dos personas. El resultado es aleatorio y no debe interpretarse como una evaluación real. Utilizando un algoritmo "avanzado" (pero completamente aleatorio 😉), te da un resultado humorístico junto con un consejo romántico.

---

## **📌 Propósito**

Esta aplicación fue creada con los siguientes objetivos:
1. **Entretenimiento**: Ofrecer un momento divertido para compartir con amigos, pareja o familia.
2. **Ejemplo Educativo**: Demostrar cómo construir una interfaz gráfica con **PyQt6** y estilizarla con **QSS**.
3. **Práctica de Desarrollo**: Implementar una aplicación funcional con animaciones, estilos y lógica básica.

*Nota: Los resultados son aleatorios y no tienen base científica. ¡Tómalo con humor!*

---

## **✨ Características**

✅ **Interfaz Atractiva**:
   - Diseño rosado con gradientes suaves.
   - Bordes redondeados (3px) y efectos *hover*/*pressed*.
   - Adaptable al tamaño de la ventana.

✅ **Funcionalidad Básica**:
   - Ingresa dos nombres y calcula su "compatibilidad".
   - Muestra un mensaje único según el porcentaje obtenido.
   - Ofrece un consejo romántico aleatorio.

✅ **Tecnologías Usadas**:
   - **Python 3** + **PyQt6** para la interfaz gráfica.
   - **QSS** (Qt Style Sheets) para los estilos visuales.

---

## **🚀 Cómo Ejecutarlo**

### **Requisitos**
- Python 3.8 o superior.
- PyQt6 (`python -m pip install -r lib/requirements.txt`).

### **Pasos**
1. Clona o descarga el repositorio.
2. Ejecuta el script:
   ```sh
   python matchmeter.py
   ```
3. ¡Disfruta del resultado!

---

## **📝 Personalización**

Si quieres modificar la app, puedes:
🔹 **Cambiar los colores**: Edita los gradientes en `apply_styles()`.
🔹 **Añadir más frases**: Modifica la lista `frases` en `get_random_advice()`.
🔹 **Cambiar los mensajes de compatibilidad**: Edita `get_message_and_emoji()`.

---

## **📜 Licencia**

Este proyecto es de **código abierto** bajo la licencia **MIT**. ¡Siéntete libre de usarlo y modificarlo!

---

## **💬 ¿Preguntas o Sugerencias?**

¡Déjalas en los *issues* del repositorio o contribuye con un *pull request*!

**¡Que el amor (y el código) estén contigo! 💖**

---

📂 **Repositorio**: [github.com/jesusquijada34/matchmeter](https://github.com/jesusquijada34/matchmeter)

🔹 **Versión**: v1.0 AlphaCube (fuente portable para Linux y Windows)
🔹 **Autor**: Jesus Quijada
🔹 **Fecha**: 12 Agosto 2024

---

### **📌 Nota Final**
*"El amor no tiene algoritmo, pero un poco de diversión sí."* 😄
