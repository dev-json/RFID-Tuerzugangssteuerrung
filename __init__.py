import utils.jxutils as jx
import time
import sys
import pages.interfaces as intf
import utils.dsql.dsql as sql

from rfid.rfid_service import RFID, RFIDOperational
from entities.door import Door, DoorOperational

def main():
    try:
        sql.query('SELECT "1"')
    except:
        print("Unable to establish db-connection!")
        return
    interrupt = False
    try:
        jx.__print_logo()
        while interrupt is not True:
            print_menu()
            handleLogic(jx.user_input("[?]"))
    except KeyboardInterrupt:
        interrupt = True
    finally:
        print('Bye Bye!')
        jx.__print_logo()

def print_menu():
    print()
    print("[1] - Open Interface")
    print("[2] - Start RFID-Service")
    print("[X] - Close Application")
    print("")

def handleLogic(option):
    if option.lower() == "x": 
        sys.exit(0)
    elif option == '1' or option == '2':
        if option == '1':
            intf.print_menu()
        elif option == '2':
            print('Trying to start rfid-service..')
            time.sleep(1)
            configured_door = None
            if configured_door is None:
                print('No configured door found!')
                time.sleep(0.5)
                print('Please enter a door-id')
                door_found = False
                while not door_found: 
                    door_id = jx.user_input()
                    if DoorOperational.is_door_exists(door_id):
                        door_found = True
                        print('DOOR_FOUND')
                        time.sleep(1)
                        configured_door = Door(door_id)
                    else:
                        print('DOOR_NOT_EXISTS')
                        print('Please try again!')
            print('START_SERVICE')
            service = RFID(configured_door)
            service.start_service()
    else:
        print("Invalid Option choosen, please try again!")
        time.sleep(1)

if __name__ == "__main__":
    main()