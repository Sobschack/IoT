import RPi.GPIO as GPIO
import time

# Configuration des GPIO
IN1 = 17  # GPIO pour contrôler la direction du moteur
IN2 = 27  # GPIO pour contrôler la direction du moteur
EN1 = 22  # GPIO pour le signal PWM (Enable pin)

# Définir la vitesse du moteur en pourcentage (0 à 100)
vitesse = 25  # Modifier cette valeur pour ajuster la vitesse

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(EN1, GPIO.OUT)

# Configuration PWM sur EN1 à 1000Hz
pwm = GPIO.PWM(EN1, 1000)
pwm.start(0)  # Démarre le PWM avec un rapport cyclique de 0%

def set_motor_speed(duty_cycle):
    pwm.ChangeDutyCycle(duty_cycle)

def set_motor_direction(forward):
    if forward:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)

try:
    while True:
        print(f"Moteur avant à {vitesse}% de vitesse")
        set_motor_direction(True)
        set_motor_speed(vitesse)  # Applique la vitesse définie
        time.sleep(5)

        print(f"Moteur arrière à {vitesse}% de vitesse")
        set_motor_direction(False)
        set_motor_speed(vitesse)  # Applique la vitesse définie
        time.sleep(5)

        print("Arrêt du moteur")
        set_motor_speed(0)  # Arrêt du moteur en mettant le PWM à 0%
        time.sleep(2)

except KeyboardInterrupt:
    print("Arrêt du programme")
finally:
    pwm.stop()
    GPIO.cleanup()
#Speed variable
