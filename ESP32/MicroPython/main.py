from machine import Pin, I2C
import framebuf
from ssd1306 import SSD1306_I2C

# Configuration de l'I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Initialisation de l'écran SSD1306
oled = SSD1306_I2C(128, 64, i2c)

# Effacer l'écran
oled.fill(0)

# Texte à afficher
text1 = "Hello"
text2 = "World"

# Fonction pour dessiner du texte
def draw_text(oled, text, x, y):
    oled.text(text, x, y)

# Calcul de la largeur du texte pour le centrage
text_width1 = len(text1) * 8
text_width2 = len(text2) * 8

# Calcul de la position pour centrer chaque texte
x1 = (oled.width - text_width1) // 2
x2 = (oled.width - text_width2) // 2

# Position verticale avec 5 pixels d'espace entre les lignes
y1 = (oled.height // 2) - 8 - 5  # Première ligne plus haute
y2 = y1 + 8 + 5  # Deuxième ligne juste en dessous avec un espace de 5 pixels

# Afficher "Hello" sur la première ligne
draw_text(oled, text1, x1, y1)

# Afficher "World" sur la deuxième ligne
draw_text(oled, text2, x2, y2)

# Mettre à jour l'affichage pour montrer le texte
oled.show()
