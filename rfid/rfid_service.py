import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import sys

from entities.door import Door
from entities.user import User, UserOperations
from entities.groups import Group, GroupOperations
from entities.transponder import Transponder
from entities.door_log import DoorLogOperational

class RFID:

    def __init__(self, door:Door):
        self.door = door

    def start_service(self):
        # Konfiguration des SPI Interfaces - siehe SPI Dokumentation/en
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False) # Deaktiviert Warnungen
        GPIO.setup(33, GPIO.OUT) # Blau
        GPIO.setup(35, GPIO.OUT) # Grün
        GPIO.setup(37, GPIO.OUT) # Rot

        GPIO.output(33, GPIO.HIGH) # Blau
        GPIO.output(35, GPIO.LOW) # Grün
        GPIO.output(37, GPIO.LOW) # Rot

        is_running = True
        print('Waiting for input!')

        reader = SimpleMFRC522()
        current_user = None
        while is_running:
            try:
                GPIO.output(33, GPIO.HIGH) # Blau
                GPIO.output(35, GPIO.LOW) # Grün
                GPIO.output(37, GPIO.LOW) # Rot
                id, content = reader.read()

                if id is not None:
                    # Diese Logik wurde eingebaut, damit der aktuelle benutzer "gecached" wird bis ein anderer Benutzer angefragt wird
                    if current_user is None or current_user.transponder is not content:
                        transponder = Transponder(content)
                        current_user = UserOperations.get_user_from_transponder(transponder)
                    
                    if UserOperations.has_door_access(current_user, self.door):
                        GPIO.output(33, GPIO.LOW) # Blau
                        GPIO.output(35, GPIO.HIGH) # Grün
                        GPIO.output(37, GPIO.LOW) # Rot
                        print('ACCESS_GRANTED')
                        time.sleep(5)
                    else:

                        DoorLogOperational.write_log_entry(self.door.id, current_user.id, 'ACCESS_ATTEMPT_FAILED')
                        
                        GPIO.output(33, GPIO.LOW) # Blau
                        GPIO.output(35, GPIO.LOW) # Grün
                        GPIO.output(37, GPIO.HIGH) # Rot
                        print('ACCESS_DENIED')
                        time.sleep(5)
            except Exception:
                GPIO.output(33, GPIO.LOW) # Blau
                GPIO.output(35, GPIO.LOW) # Grün
                GPIO.output(37, GPIO.HIGH) # Rot
                time.sleep(5)
            except KeyboardInterrupt as e:
                GPIO.cleanup()
                raise e

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
