import RPi.GPIO as GPIO
import time

# Configuration des GPIO
GPIO.setmode(GPIO.BCM)  # Utilisation de la numérotation BCM
GPIO.setwarnings(False)

# Définition des broches
MOTOR_PIN1 = 17  # IN1 du L293D
MOTOR_PIN2 = 27  # IN2 du L293D
BUTTON_PIN = 22  # Bouton poussoir

# Configuration des broches
GPIO.setup(MOTOR_PIN1, GPIO.OUT)
GPIO.setup(MOTOR_PIN2, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Tirage au niveau haut pour le bouton

def motor_on():
    GPIO.output(MOTOR_PIN1, GPIO.HIGH)
    GPIO.output(MOTOR_PIN2, GPIO.LOW)

def motor_off():
    GPIO.output(MOTOR_PIN1, GPIO.LOW)
    GPIO.output(MOTOR_PIN2, GPIO.LOW)

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Bouton appuyé
            motor_on()
        else:
            motor_off()
        time.sleep(0.1)  # Petite pause pour éviter une boucle trop rapide

except KeyboardInterrupt:
    pass  # Arrêt du programme avec Ctrl+C

finally:
    motor_off()  # Arrêt du moteur avant de quitter
    GPIO.cleanup()  # Nettoyage des GPIO
