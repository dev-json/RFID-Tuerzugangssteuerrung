import utils.jxutils as jx
import time
from utils.dsql.dsql import execute, query
from entities.building import Building, BuildingOperational
from entities.room import Room, RoomOperational
from entities.door import Door, DoorOperational

interrupted = False

def print_objects_menu():
    global interrupted
    interrupted = False
    while interrupted is not True:
        jx.empty_line(20)
        print('')
        # Kann man auch alles in eine Query verfassen und via Tuple Index auslesen...
        total_count = query('SELECT total_objects FROM jperations')[0][0]
        building_count = query('SELECT count_gebaeude FROM jperations')[0][0]
        room_count = query('SELECT count_raum FROM jperations')[0][0]
        door_count = query('SELECT count_tuer FROM jperations')[0][0]
        print(f'{total_count} Total objects found')
        print(f'  - {building_count} Buildings')
        print(f'  - {room_count} Rooms')
        print(f'  - {door_count} Doors')
        print('')
        if building_count <= 0:
            print('INFO - NO_OBJECTS_FOUND')
            print('')
            print('[1] - Create building')
        else:
            print('[1] - Building(s)')
        
        if building_count > 0 and room_count <= 0:
            print('[2] - Create room') 
        else:
            if building_count > 0:
                print('[2] - Room(s)')

        if building_count > 0 and room_count > 0 and door_count <= 0:
            print('[3] - Create door') 
        else:
            if door_count > 0 and building_count > 0 :
                print('[3] - Door(s)')

        print('')
        print('[X] - Back')
        handle_logic(jx.user_input('[?]'))

def handle_logic(option):

    # Kann man auch alles in eine Query verfassen und via Tuple Index auslesen...
    total_count = query('SELECT total_objects FROM jperations')[0][0]
    building_count = query('SELECT count_gebaeude FROM jperations')[0][0]
    room_count = query('SELECT count_raum FROM jperations')[0][0]
    door_count = query('SELECT count_tuer FROM jperations')[0][0]

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
            if building_count <= 0:
                create_building()
                return
            else:
                show_extended_settings = True
                while show_extended_settings is not False:
                    jx.empty_line(20)
                    print('')
                    print('[1] - Create building')
                    print('[2] - Modify building')
                    print('[3] - Delete building')
                    print('')
                    print('[X] - Back')
                    extended_option = jx.user_input()
                    if extended_option.lower() == 'x': 
                        show_extended_settings = False
                        return
                    try: int(extended_option) 
                    except ValueError: 
                        print('Please provide a valid input!')
                        time.sleep(1)
                        return
                    if 1 <= int(extended_option) <= 3:
                        if extended_option == '1':
                            create_building()
                        elif extended_option == '2':
                            print('[Gebäude-ID]')
                            building_id = jx.user_input()
                            if not BuildingOperational.is_building_exists(building_id) :
                                print('OBJECT_NOT_EXISTS')
                                continue
                            print('')
                            print('Enter new Description:')
                            new_description = jx.user_input()
                            building = Building(building_id)
                            building.set_description(new_description)
                            print('OBJECT_UPDATED')
                        elif extended_option == '3':
                            print('[Gebäude-ID]')
                            building_id = jx.user_input()
                            if not BuildingOperational.is_building_exists(building_id) :
                                print('OBJECT_NOT_EXISTS')
                                continue
                            print('')
                            print('BE CAREFUL - DELETING THIS OBJECT WILL SET ALL ITS REFERENCES TO \'NULL\'!')
                            print('')
                            print('Continue? [Y/N]')

                            if jx.user_input().lower() == 'n':
                                print('ABORTED')
                                continue
                            print('CONFIRMED')
                            BuildingOperational.delete_building(Building(building_id))
                            print('OBJECT_DELETED')
                            time.sleep(1)
                            # Falls der BuildingCount auf 0 geriert, betrete "objects-menu"
                            if building_count <= 0:
                                return
                        else:
                            print("Invalid Option choosen, please try again!")
                            time.sleep(1)
        if option == '2':
            if building_count <= 0:
                print('NO_BUILDING_FOUND')
                return
            
            if room_count <= 0:
                create_room()
            else:
                show_extended_settings = True
                while show_extended_settings is not False:
                    jx.empty_line(20)
                    print('')
                    print('[1] - Create room')
                    print('[2] - Modify room')
                    print('[3] - Delete room')
                    print('')
                    print('[X] - Back')
                    extended_option = jx.user_input()
                    if extended_option.lower() == 'x': 
                        show_extended_settings = False
                        return
                    try: int(extended_option) 
                    except ValueError: 
                        print('Please provide a valid input!')
                        time.sleep(1)
                        return
                    if 1 <= int(extended_option) <= 3:
                        if extended_option == '1':
                            create_room()
                        elif extended_option == '2':
                            print('[Raum-ID]')
                            room_id = jx.user_input()
                            if not RoomOperational.is_room_exists(room_id) :
                                print('OBJECT_NOT_EXISTS')
                                continue
                            show_sub_room_settings = True
                            while show_sub_room_settings is not False:
                                jx.empty_line(20)
                                print('')
                                print('[1] - Edit description')
                                print('[2] - Edit building')
                                print('')
                                print('[X] - Back')

                                sub_option = jx.user_input()
                                
                                if sub_option.lower() == 'x':
                                    show_sub_room_settings = False
                                    continue
                                if sub_option == '1':
                                    print('Please enter your description')
                                    new_description = jx.user_input()
                                    room = Room(room_id)
                                    room.set_description(new_description)
                                    print('OBJECT_UPDATED')
                                    continue
                                elif sub_option == '2':
                                    print('Please enter your new [Gebäude-ID]')
                                    building_id = jx.user_input()
                                    if BuildingOperational.is_building_exists(building_id):
                                        building = Building(building_id)
                                        room = Room(room_id)
                                        room.set_building(building)
                                        print('OBJECT_UPDATED')
                                        continue
                                else:
                                    print("Invalid Option choosen, please try again!")
                                    time.sleep(1)
                        elif extended_option == '3':
                            print('[Raum-ID]')
                            room_id = jx.user_input()
                            if not RoomOperational.is_room_exists(room_id) :
                                print('OBJECT_NOT_EXISTS')
                                continue
                            print('')
                            print('BE CAREFUL - DELETING THIS OBJECT WILL SET ALL ITS REFERENCES TO \'NULL\'!')
                            print('')
                            print('Continue? [Y/N]')

                            if jx.user_input().lower() == 'n':
                                print('ABORTED')
                                continue
                            print('CONFIRMED')
                            RoomOperational.delete_room(Room(room_id))
                            print('OBJECT_DELETED')
                            time.sleep(1)
                            # Falls der BuildingCount auf 0 geriert, betrete "objects-menu"
                            if room_count <= 0:
                                return
                        else:
                            print("Invalid Option choosen, please try again!")
                            time.sleep(1)
                pass
        if option == '3':
            if room_count <= 0:
                print('NO_ROOM_FOUND')
                return
            
            if door_count <= 0:
                create_door()
            else:
                show_extended_settings = True
                while show_extended_settings is not False:
                    jx.empty_line(20)
                    print('')
                    print('[1] - Create door')
                    print('[2] - Modify door')
                    print('[3] - Delete door')
                    print('')
                    print('[X] - Back')
                    extended_option = jx.user_input()
                    if extended_option.lower() == 'x': 
                        show_extended_settings = False
                        return
                    try: int(extended_option) 
                    except ValueError: 
                        print('Please provide a valid input!')
                        time.sleep(1)
                        return
                    if 1 <= int(extended_option) <= 3:
                        if extended_option == '1':
                            create_door()
                        elif extended_option == '2':
                            print('[Tür-ID]')
                            door_id = jx.user_input()
                            if not DoorOperational.is_door_exists(door_id) :
                                print('OBJECT_NOT_EXISTS')
                                continue
                            show_sub_door_settings = True
                            while show_sub_door_settings is not False:
                                jx.empty_line(20)
                                print('')
                                print('[1] - Edit description')
                                print('[2] - Edit room')
                                print('')
                                print('[X] - Back')

                                sub_option = jx.user_input()
                                
                                if sub_option.lower() == 'x':
                                    show_sub_door_settings = False
                                    continue
                                if sub_option == '1':
                                    print('Please enter your description')
                                    new_description = jx.user_input()
                                    door = Door(door_id)
                                    door.set_description(new_description)
                                    print('OBJECT_UPDATED')
                                    continue
                                elif sub_option == '2':
                                    print('Please enter your new [Raum-ID]')
                                    room_id = jx.user_input()
                                    if RoomOperational.is_room_exists(room_id):
                                        room = Room(room_id)
                                        door = Door(door_id)
                                        door.set_room(room)
                                        print('OBJECT_UPDATED')
                                        continue
                                else:
                                    print("Invalid Option choosen, please try again!")
                                    time.sleep(1)
                        elif extended_option == '3':
                            print('[Tür-ID]')
                            door_id = jx.user_input()
                            if not DoorOperational.is_door_exists(door_id) :
                                print('OBJECT_NOT_EXISTS')
                                continue
                            print('')
                            print('BE CAREFUL - DELETING THIS OBJECT WILL SET ALL ITS REFERENCES TO \'NULL\'!')
                            print('')
                            print('Continue? [Y/N]')

                            if jx.user_input().lower() == 'n':
                                print('ABORTED')
                                continue
                            print('CONFIRMED')
                            DoorOperational.delete_door(Door(door_id))
                            print('OBJECT_DELETED')
                            time.sleep(1)
                            # Falls der BuildingCount auf 0 geriert, betrete "objects-menu"
                            if door_count <= 0:
                                return
                        else:
                            print("Invalid Option choosen, please try again!")
                            time.sleep(1)
                pass
        else:
            print("Invalid Option choosen, please try again!")
            time.sleep(1)
def create_building():
    # Erstelle Gebäude
    gebaeude_id = jx.user_input('[Gebäude-ID]')
    if BuildingOperational.is_building_exists(gebaeude_id):
        print('OBJECT_ALREADY_EXISTS')
        time.sleep(1)
        return
    
    print('Please provide us a building description')
    building_description = jx.user_input('[?]')
    building = Building(gebaeude_id)
    building.set_description(building_description)
    print('OBJECT_CREATED')

# Erstelle Raum
def create_room():
    room_id = jx.user_input('[Raum-ID]')
    if RoomOperational.is_room_exists(room_id):
            print('OBJECT_ALREADY_EXISTS')
            time.sleep(1)
            return
    
    print('Please provide us a room description')
    room_description = jx.user_input('[?]')
    room = Room(room_id)
    room.set_description(room_description)

    print('Connect room to a building? [Y/N]')

    connect_building = jx.user_input('[?]')

    if connect_building.lower() == 'y':
        assigned = False
        print('Press enter to exit this prompt')
        while assigned is not True: 
            building_id = jx.user_input('[Gebäude-ID]')
            if building_id == '':
                break
            if BuildingOperational.is_building_exists(building_id):
                room.set_building(Building(building_id))
                assigned = True
            else:
                jx.empty_line(10)
                print('OBJECT_NOT_EXISTS')
                jx.empty_line(1)
    print('OBJECT_CREATED')

# Erstelle Tür
def create_door():
    door_id = jx.user_input('[Tür-ID]')
    if DoorOperational.is_door_exists(door_id):
        print('OBJECT_ALREADY_EXISTS')
        time.sleep(1)
        return
                
    print('Please provide us a door description')
    door_description = jx.user_input('[?]')
    door = Door(door_id)
    door.set_description(door_description)

    print('Connect door to a room? [Y/N]')

    connect_room = jx.user_input('[?]')

    if connect_room.lower() == 'y':
        assigned = False
        print('Press enter to exit this prompt')
        while assigned is not True: 
            room_id = jx.user_input('[Raum-ID]')
            if room_id == '':
                break
            if RoomOperational.is_room_exists(room_id):
                door.set_room(Room(room_id))
                assigned = True
            else:
                jx.empty_line(10)
                print('OBJECT_NOT_EXISTS')
                jx.empty_line(1)
    print('OBJECT_CREATED')