import utils.jxutils as jx
import time
from utils.dsql.dsql import execute, query
from entities.groups import Group, GroupOperations

interrupted = False

def print_groups_menu():
    global interrupted
    interrupted = False
    while interrupted is not True:
        jx.empty_line(20)
        group_count = query('SELECT count_gruppe FROM jperations')[0][0]
        print(f'{group_count} groups found')
        print()
        print('[1] - Create group')
        if group_count > 0:
            print('[2] - Edit group')
            print('[3] - Remove group')
        print('')
        print('[X] - Go back')
        
        handle_logic(jx.user_input('[?]'))

def handle_logic(option):
    global interrupted
    if option.lower() == 'x': 
        interrupted = True
        return
    try: int(option) 
    except ValueError: 
        print('Please provide a valid input!')
        time.sleep(1)
        return
    if 1 <= int(option) <= 3:
        if option == '1':
            create_group()
        elif option == '2':
            modify_group()
        elif option == '3':
            delete_group()
        else:
            print('Invalid Option choosen, please try again!')
            time.sleep(1)
def create_group():
    group_no = jx.user_input('[Gruppen-Nummer]')

    if GroupOperations.is_group_exists(group_no):
        print('GROUP_ALREADY_EXISTS')
        return
    
    group = Group(group_no)
    print('Please insert a group name')
    print()
    group_name = jx.user_input("[Gruppen-Name]")

    group.set_name(group_name)
    print("GROUP_CREATED")

def delete_group():
    group_no = jx.user_input('[Gruppen-Nummer]')

    if not GroupOperations.is_group_exists(group_no):
        print('GROUP_NOT_EXISTS')
        return
    
    group = Group(group_no)
    GroupOperations.delete_group(group)
    print("GROUP_DELETED")
        
def modify_group():
    group_no = jx.user_input('[Gruppen-Nummer]')

    if not GroupOperations.is_group_exists(group_no):
        print('GROUP_NOT_EXISTS')
        return
    
    group = Group(group_no)

    show_extended_settings = True
    while show_extended_settings:
        print('')
        print(f'Modifying group: {group.name}')
        print('')
        print('[1] - Change name')
        print('[2] - Modify group members')
        print('[3] - Door accesses')
        print('')
        print('[X] - Go back')

        selection = jx.user_input()
        if selection.lower() == 'x': 
            show_extended_settings = False
            return
        try: int(selection) 
        except ValueError: 
            print('Please provide a valid input!')
            time.sleep(1)
            return
        if 1 <= int(selection) <= 3:
            if selection == '1':
                new_name = jx.user_input('[Gruppen-Name]')
                group.set_name(new_name)
                print("GROUP_UPDATED")
                continue
            elif selection == '2':
                
                continue
            elif selection == '3':

                continue
            else:
                print('Invalid Option choosen, please try again!')
                time.sleep(1)