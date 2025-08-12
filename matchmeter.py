import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QLabel, QLineEdit, QPushButton, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QLinearGradient, QBrush
icon = "app/app-icon.ico"
class MatchMeterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MatchMeter 💖")
        self.setWindowIcon(QIcon(icon))  # Make sure to have this file
        self.resize(450, 500)

        # Main widget with central frame
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout with margins
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(60, 60, 60, 60)

        # Central frame (will contain all content)
        self.central_frame = QFrame()
        self.central_frame.setObjectName("centralFrame")
        self.main_layout.addWidget(self.central_frame)

        # Layout for central frame
        self.frame_layout = QVBoxLayout(self.central_frame)
        self.frame_layout.setContentsMargins(30, 30, 30, 30)
        self.frame_layout.setSpacing(20)

        # Title
        self.title = QLabel("💖 MatchMeter 💖")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("titleLabel")

        # Input fields
        self.name1 = QLineEdit()
        self.name1.setPlaceholderText("Tu nombre")
        self.name1.setObjectName("nameInput")

        self.name2 = QLineEdit()
        self.name2.setPlaceholderText("Nombre de tu pareja")
        self.name2.setObjectName("nameInput")

        # Button
        self.button = QPushButton("Verificar Compatibilidad")
        self.button.setObjectName("mainButton")

        # Result frame
        self.result_frame = QFrame()
        self.result_frame.setObjectName("resultFrame")
        self.result_frame.setVisible(False)
        self.result_layout = QVBoxLayout(self.result_frame)
        self.result_layout.setContentsMargins(15, 15, 15, 15)
        self.result_layout.setSpacing(10)

        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setObjectName("resultLabel")

        self.advice_label = QLabel()
        self.advice_label.setWordWrap(True)
        self.advice_label.setAlignment(Qt.AlignCenter)
        self.advice_label.setObjectName("adviceLabel")

        self.result_layout.addWidget(self.result_label)
        self.result_layout.addWidget(self.advice_label)

        # Add widgets to layout
        self.frame_layout.addWidget(self.title)
        self.frame_layout.addWidget(self.name1)
        self.frame_layout.addWidget(self.name2)
        self.frame_layout.addWidget(self.button)
        self.frame_layout.addWidget(self.result_frame)
        self.frame_layout.addStretch()

        # Connect button
        self.button.clicked.connect(self.calculate_compatibility)

        # Apply styles
        self.apply_styles()

    def apply_styles(self):
        # Set pink background gradient for main window
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 200, 220))  # Light pink
        gradient.setColorAt(1, QColor(255, 150, 200))  # Medium pink

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Apply stylesheet
        self.setStyleSheet("""
            #centralFrame {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 5px;
                border: 1px solid #ff69b4;
            }

            #titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #d63384;
                margin-bottom: 20px;
            }

            #nameInput {
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid #ff69b4;
                border-radius: 3px;
                padding: 10px;
                color: #d63384;
                font-size: 16px;
            }

            #nameInput:hover {
                border: 1px solid #ff1493;
                background-color: white;
            }

            #nameInput:focus {
                border: 1px solid #c71585;
                background-color: white;
            }

            #mainButton {
                background-color: #ff69b4;
                color: white;
                border: 1px solid #d63384;
                border-radius: 3px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }

            #mainButton:hover {
                background-color: #ff1493;
                border: 1px solid #c71585;
            }

            #mainButton:pressed {
                background-color: #c71585;
                border: 1px solid #8b0a50;
            }

            #resultFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 3px;
                border: 1px solid #ff69b4;
            }

            #resultLabel {
                font-size: 18px;
                color: #d63384;
                font-weight: bold;
            }

            #adviceLabel {
                font-size: 14px;
                color: #d63384;
                font-style: italic;
            }
        """)

    def calculate_compatibility(self):
        if not self.name1.text() or not self.name2.text():
            return

        self.result_frame.setVisible(False)

        porcentaje = random.randint(0, 100)
        mensaje, emoji = self.get_message_and_emoji(porcentaje)
        frase_aleatoria = self.get_random_advice()

        self.result_label.setText(
            f"<strong>Resultado:</strong> {porcentaje}% - {mensaje} {emoji}"
        )

        self.advice_label.setText(
            f"<em>🧠 Consejo:</em> \"{frase_aleatoria}\""
        )

        self.result_frame.setVisible(True)

    def get_message_and_emoji(self, percentage):
        if percentage >= 90:
            return "¡Almas gemelas!", "💍💑"
        elif percentage >= 80:
            return "Flechados!", "🎯🌀"
        elif percentage >= 70:
            return "Un alma cerca tuyo", "👻🌊"
        elif percentage >= 60:
            return "Pareja perfecta", "👥💕"
        elif percentage >= 50:
            return "Mejores amigos", "❤️💫"
        elif percentage >= 40:
            return "Son amigos", "💞✨"
        elif percentage >= 30:
            return "Es algo infiel", "👎🧐"
        elif percentage >= 20:
            return "Aquella persona tiene pareja", "🐺🔮"
        elif percentage >= 10:
            return "Encontré infidelidad", "💔🤷"
        else:
            return "Nada que ver", "😅🚫"

    def get_random_advice(self):
        frases = [
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
        ]
        return random.choice(frases)

    def resizeEvent(self, event):
        # Update gradient when window is resized
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 200, 220))
        gradient.setColorAt(1, QColor(255, 150, 200))

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set font for the entire application
    font = QFont("Roboto", 10)
    app.setFont(font)

    window = MatchMeterApp()
    window.show()
    sys.exit(app.exec_())
