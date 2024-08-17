import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

LED_PIN = 17
BUTTON_PIN = 27

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configuration en pull-up interne

clignotement_actif = False
derniere_etat_bouton = GPIO.HIGH
debounce_time = 0.2  # Temps pour éviter les rebonds du bouton (200 ms)
clignotement_thread = None

def led_blink():
    while clignotement_actif:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)

def toggle_clignotement():
    global clignotement_actif, clignotement_thread
    if clignotement_actif:
        clignotement_actif = False
        if clignotement_thread is not None:
            clignotement_thread.join()  # Attendre que le thread de clignotement se termine
        GPIO.output(LED_PIN, GPIO.LOW)  # Assurez-vous que la LED est éteinte
    else:
        clignotement_actif = True
        clignotement_thread = threading.Thread(target=led_blink)
        clignotement_thread.start()

try:
    while True:
        etat_bouton = GPIO.input(BUTTON_PIN)
        
        if etat_bouton == GPIO.LOW and derniere_etat_bouton == GPIO.HIGH:
            # Le bouton vient d'être pressé
            toggle_clignotement()  # Basculer l'état du clignotement
            
        derniere_etat_bouton = etat_bouton
        time.sleep(debounce_time)  # Anti-rebond pour éviter plusieurs détections du même appui

except KeyboardInterrupt:
    GPIO.cleanup()
