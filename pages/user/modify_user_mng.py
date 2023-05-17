import utils.jxutils as jx
import time

from utils.dsql.dsql import query, execute
from entities.user import User, UserOperations
from entities.transponder import Transponder, TransponderOperations
from entities.groups import Group, GroupOperations
from entities.door import Door, DoorOperational
from rfid.rfid_service import RFIDOperational

interrupted = False

def print_modify_usr_menu(user:User):
    global interrupted
    interrupted = False
    while interrupted is not True:
        jx.empty_line(20)
        if UserOperations.has_transponder(user):
            user_transponder = Transponder(user.transponder)
            if TransponderOperations.is_transponder_locked(user_transponder):
                print('[1] Unlock transponder')
            else:
                print('[1] Lock transponder')
        else:
            print('[1] Assign transponder')
        print('[2] Group/permissions')
        print()
        print('[X] Back')
        handle_logic(jx.user_input('[?]'), user)

def handle_logic(option, user:User):
    global interrupted
    if option.lower() == "x": 
        interrupted = True
        return
    try: int(option) 
    except ValueError: 
        print("Please provide a valid input!")
        time.sleep(1)
        return
    if 1 <= int(option) <= 2:
        if option == '1':
            if UserOperations.has_transponder(user): 
                user_transponder = Transponder(user.transponder)
                if TransponderOperations.is_transponder_locked(user_transponder):
                    TransponderOperations.unlock_transponder(user_transponder, None)
                    print("TRANSPONDER_UNLOCKED")
                    return
                else:
                    TransponderOperations.lock_transponder(user_transponder, None)
                    print("TRANSPONDER_LOCKED")
                    return
            else:
                print("Please scan your transponder")
                time.sleep(1)
                card_input = RFIDOperational.wait_for_single_input()
                found_transponder = Transponder(card_input[1])
                UserOperations.assign_transponder(user, found_transponder)
                print("TRANSPONDER_MOVED")
        elif option == '2':
            show_extended_settings = True
            while show_extended_settings:
                assigned_groups = query(f'SELECT COUNT(*) FROM nutzer_gruppen ng INNER JOIN nutzer n ON n.id = ng.nutzer_id WHERE n.nutzer_no = \'{user.user_no}\'')
                accessable_doors = query(f'SELECT COUNT(*) FROM nutzer_tuer_zugriff ntz INNER JOIN nutzer n ON n.id = ntz.nutzer_id WHERE n.nutzer_no = \'{user.user_no}\'')
                print('')
                print(f'{assigned_groups[0][0]} assigned groups')
                print(f'{accessable_doors[0][0]} accessable doors')
                print('')
                print('[1] - Add group')
                print('[2] - Remove group')
                print('[3] - Add door access')
                print('[4] - Remove door access')
                print()
                print(f'[X] - Back')
                selection = jx.user_input()

                if selection.lower() == "x": 
                    show_extended_settings = False
                    continue
                try: int(selection) 
                except ValueError: 
                    print("Please provide a valid input!")
                    time.sleep(1)
                    continue
                if 1 <= int(selection) <= 4:
                    if selection == '1':
                        gruppen_id = jx.user_input('[Gruppen-ID]')
                        if not GroupOperations.is_group_exists(gruppen_id):
                            print("GROUP_NOT_EXISTS")
                            continue
                        group = Group(gruppen_id)
                        if UserOperations.is_in_group(user, group):
                            print('USER_ALREADY_IN_GROUP')
                            continue
                        UserOperations.assign_to_group(user, group)
                    elif selection == '2':
                        gruppen_id = jx.user_input('[Gruppen-ID]')
                        if not GroupOperations.is_group_exists(gruppen_id):
                            print("GROUP_NOT_EXISTS")
                            continue
                        group = Group(gruppen_id)
                        if not UserOperations.is_in_group(user, group):
                            print('USER_NOT_IN_GROUP')
                            continue
                        UserOperations.remove_from_group(user, group)
                    elif selection == '3':
                        door_id = jx.user_input('[Tür-ID]')
                        if not DoorOperational.is_door_exists(door_id):
                            print('DOOR_NOT_EXISTS')
                            continue
                        door = Door(door_id)
                        if UserOperations.has_door_access(user, door):
                            print('USER_ALREADY_HAS_ACCESS')
                            continue

                        UserOperations.add_door_access(user, door)
                        print('ACCESS_GRANTED')
                    elif selection == '4':
                        door_id = jx.user_input('[Tür-ID]')
                        if not DoorOperational.is_door_exists(door_id):
                            print('DOOR_NOT_EXISTS')
                            continue
                        door = Door(door_id)
                        if not UserOperations.has_door_access(user, door):
                            print('USER_HAS_NO_HAS_ACCESS')
                            continue

                        UserOperations.remove_door_access(user, door)
                        print('ACCESS_REVOKED')
                    else:
                        print('Invalid Option choosen, please try again!')
                        time.sleep(1)
        else: 
            print('Invalid Option choosen, please try again!')
            time.sleep(1)
