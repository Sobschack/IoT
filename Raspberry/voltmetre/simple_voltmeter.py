import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Initialisation I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialisation de l'écran OLED SSD1306
oled = SSD1306_I2C(128, 64, i2c)

# Création d'une image vide pour dessiner
image = Image.new('1', (oled.width, oled.height))  # '1' pour image en niveaux de gris
draw = ImageDraw.Draw(image)

# Chargement d'une police plus grande
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
except IOError:
    font = ImageFont.load_default()

# Initialisation de l'ADS1115
ads = ADS1115(i2c)

# Définir le gain pour une plage de ±1.024V
ads.gain = 4  # ±1.024V

# Facteur correctif
correction_factor = 1.188679245283019

# Fonction pour lire la tension depuis le canal spécifié
def read_voltage(channel):
    # Lire la valeur brute du canal spécifié
    value = ads.read(channel)
    
    # Convertir la valeur brute en tension
    max_adc_value = 32767  # Valeur maximale pour 16 bits
    max_voltage = 1.024  # Plage maximale pour le gain = 4
    voltage = (value / max_adc_value) * max_voltage
    
    # Appliquer le facteur correctif
    corrected_voltage = voltage * correction_factor
    return corrected_voltage

# Fonction pour afficher la tension sur l'écran OLED
def display_voltage(voltage):
    # Effacer l'image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    
    # Dessiner le texte centré
    text = f'{voltage:.2f} V'
    # Utiliser textbbox pour obtenir les dimensions du texte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculer les coordonnées pour centrer le texte
    x = (oled.width - text_width) // 2
    y = (oled.height - text_height) // 2
    draw.text((x, y), text, font=font, fill=255)
    
    # Afficher l'image sur l'écran OLED
    oled.image(image)
    oled.show()

# Fonction principale avec gestion de Ctrl+C
def main():
    start_time = time.time()
    try:
        while True:
            # Lire la valeur de la tension depuis le canal 1 (A1)
            voltage = read_voltage(1)  # Canal 1 (A1)
            
            # Afficher la tension
            display_voltage(voltage)
            
            # Attendre pour maintenir la fréquence d'affichage de 10 Hz (100 ms)
            elapsed_time = time.time() - start_time
            sleep_time = max(0, (1 / 10) - elapsed_time % (1 / 10))
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        # Gestion de Ctrl+C pour quitter proprement
        print("\nProgramme interrompu par l'utilisateur. Arrêt en cours...")
        oled.fill(0)
        oled.show()
        print("Affichage effacé. Programme terminé.")

if __name__ == "__main__":
    main()

#v1.8
