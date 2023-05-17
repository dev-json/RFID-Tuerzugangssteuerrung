#import RPi.GPIO as GPIO
import time
#from mfrc522 import SimpleMFRC522
import sys

from entities.door import Door
from entities.user import User, UserOperations
from entities.groups import Group, GroupOperations

class RFID:

    def __init__(self, door:Door):
        self.door = door

    def start_service(self):
        # Konfiguration des SPI Interfaces - siehe SPI Dokumentation/en
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False) # Deaktiviert Warnungen
        GPIO.setup(37, GPIO.OUT)
        GPIO.setup(35, GPIO.OUT)
        GPIO.output(37, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)

        is_running = True
        print('Waiting for input!')

        reader = SimpleMFRC522()

        while is_running:
            id, content = reader.read()

            print(f'id: {id}')
            print(f'content: {content}')

            # TODO implement check logic, if user has access to this door

class RFIDOperational:

    def wait_for_single_input():
        reader = SimpleMFRC522()
        print('Waiting for chip...')
        id, content = reader.read() 
        while id is not None:
            return [id, content]
            
    def write_back(old_id, new_content):
        # Konfiguration des SPI Interfaces - siehe SPI Dokumentation/en
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False) # Deaktiviert Warnungen
        GPIO.setup(37, GPIO.OUT) # 37 Grün
        GPIO.setup(35, GPIO.OUT) # 35 Rot
        GPIO.output(37, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        written = False
        while written is not True:
            print("Waiting for chip/card")
            reader = SimpleMFRC522()

            id = reader.read()
            if id is not None:
                reader.write(new_content)
                written = True
                GPIO.output(37, GPIO.HIGH)
        time.sleep(5)
        GPIO.cleanup()
        return True
