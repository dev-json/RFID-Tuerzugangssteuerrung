import utils.jxutils as jx
import time
from utils.dsql.dsql import execute, query
from entities.user import User, UserOperations
from entities.transponder import Transponder, TransponderOperations
from rfid.rfid_service import RFIDOperational

from . modify_user_mng import print_modify_usr_menu

interrupted = False

def print_usr_menu():
    global interrupted
    interrupted = False
    while interrupted is not True:
        jx.empty_line(20)
        print('')
        user_count = query('SELECT count_user FROM jperations')
        print(f'{user_count[0][0]} Users found')
        print('')
        print('[1] - Create User')
        if user_count[0][0] > 0:
            print('[2] - Modify User')
            print('[3] - Delete User')
            print('[4] - User information')
        print('')
        print('[X] - Back')
        handleLogic(jx.user_input('[?]'))

def handleLogic(option):
    global interrupted
    if option.lower() == "x": 
        interrupted = True
        return
    try: int(option) 
    except ValueError: 
        print("Please provide a valid input!")
        time.sleep(1)
        return
    if 1 <= int(option) <= 4:
        if option == '1':
            user_no = jx.user_input("[Benutzer-Nummer]")

            if UserOperations.is_user_exists(user_no) is not True:
                user = User(user_no)
                    
                vorname = jx.user_input("[Vorname]")
                nachname = jx.user_input("[Nachname]")
                email = jx.user_input("[Email]")

                user.set_name(vorname, nachname)
                user.set_email(email)

                print('')
                print('Do you want to assign a transponder? [Y/N]')
                print('')
                assign_transponder = jx.user_input("[Y/N]")

                if assign_transponder.lower() == 'y':

                    card_input = RFIDOperational.wait_for_single_input()
                    internal_transponder_id = card_input[0]
                    transponder_content = card_input[1]    

                    found_transponder = Transponder(transponder_content)
                    if RFIDOperational.write_back(internal_transponder_id, str(found_transponder.id)):
                        print("TRANSPONDER_CONFIGURED")
                    UserOperations.assign_transponder(user, found_transponder)
                print("USER_CREATED")
                time.sleep(1)
                pass
            else:
                print('USER_ALREADY_EXISTS')
                time.sleep(1)
                pass
        if option == '2':
            user_no = jx.user_input("[Benutzer-Nummer]")

            if UserOperations.is_user_exists(user_no) is not True:
                print("USER_NOT_EXISTS!")
                time.sleep(1)
                return
            user = User(user_no)
            print_modify_usr_menu(user)

        if option == '3':
            user_no = jx.user_input("[Benutzer-Nummer]")

            if UserOperations.is_user_exists(user_no) is not True:
                print("USER_NOT_EXISTS!")
                time.sleep(1)
                return
            
            user = User(user_no)
            UserOperations.delete_user(user)
            print("USER_DELETED")

        if option == '4':
            user_no = jx.user_input("[Benutzer-Nummer]")

            if UserOperations.is_user_exists(user_no) is not True:
                print("USER_NOT_EXISTS!")
                time.sleep(1)
                return

            user = User(user_no)
            jx.empty_line(50)
            print('-----------------------')
            print(f'User-No: {user.user_no}')
            print(f'Name: {user.firstname}, {user.lastname}')
            print(f'Email: {user.email}')
            print(f'Transponder: {user.transponder}')
            if user.transponder is not None:
                user_transponder = Transponder(user.transponder)
                print(f'  - is_locked = {TransponderOperations.is_transponder_locked(user_transponder)}')
            print('')
            assigned_groups = query(f'SELECT COUNT(*) FROM nutzer_gruppen ng INNER JOIN nutzer n ON n.id = ng.nutzer_id WHERE n.nutzer_no = \'{user.user_no}\'')
            if assigned_groups[0][0] > 0:
                assigned_group_names = UserOperations.get_groups(user)
                print('Zugewiesene Gruppen: ')
                for name in assigned_group_names[0]:
                    print(f'  - {name}')
            print('')
            print(f'ID: {user.id}')
            print('-----------------------')
            print('')
            print('Press enter to go back')
            input()
            pass
    else:
        print("Invalid Option choosen, please try again!")
        time.sleep(1)
    


