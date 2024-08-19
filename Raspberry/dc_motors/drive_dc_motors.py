import RPi.GPIO as GPIO
import time

# Configuration des GPIO
IN1 = 17  # GPIO pour contrôler la direction du moteur
IN2 = 27  # GPIO pour contrôler la direction du moteur

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

def set_motor_direction(forward):
    if forward:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)

try:
    while True:
        print("Moteur avant")
        set_motor_direction(True)  # Faire tourner le moteur vers l'avant
        time.sleep(5)

        print("Moteur arrière")
        set_motor_direction(False)  # Faire tourner le moteur vers l'arrière
        time.sleep(5)

        print("Arrêt moteur")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)  # Arrêt du moteur
        time.sleep(2)

except KeyboardInterrupt:
    print("Arrêt du programme")
finally:
    GPIO.cleanup()
