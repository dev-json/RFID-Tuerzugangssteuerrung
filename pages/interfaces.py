import time
import utils.jxutils as jx
from . user.user_mng import print_usr_menu
from . objects.objects_mng import print_objects_menu
from . groups.groups_mng import print_groups_menu

interrupted = False

def print_menu():
    global interrupted
    interrupted = False
    while interrupted is not True:
        jx.empty_line(20)
        print('[1] - User')
        print('[2] - Groups')
        print('[3] - Objects (Doors/Rooms/Buildings)')
        print('')
        print('[X] - Go back')
        
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
    if 1 <= int(option) <= 3:
        if option == '1':
            print_usr_menu()
        elif option == '2':
            print_groups_menu()
        elif option == '3':
            print_objects_menu()
    else:
        print("Invalid Option choosen, please try again!")
        time.sleep(1)