from utils.dsql.dsql import execute, query

from .room import Room

class Door:
    
    def __init__(self, id):
        self.id = id
        self.description = None
        self.room = None

        if not DoorOperational.is_door_exists(self.id):
            self.__create_database_entry()
        else:
            self.description = query(f'SELECT beschreibung FROM tuer WHERE id = \'{self.id}\'')[0][0]

    def __create_database_entry(self):
        execute(f'INSERT INTO tuer(id) VALUES (\'{self.id}\')')

    def set_description(self, description = None):
        if description is not None:
            self.description = description
            execute(f'UPDATE tuer SET beschreibung = \'{description}\' WHERE id = \'{self.id}\'')
    
    def set_room(self, room:Room = None):
        if room is not None:
            self.room = room.id
            execute(f'UPDATE tuer SET raum_id = \'{room.id}\' WHERE id = \'{self.id}\'')
class DoorOperational:
    
    @classmethod
    def is_door_exists(cls, door_id):
        if query(f'SELECT COUNT(id) FROM tuer WHERE id = \'{door_id}\'')[0][0] > 0:
            return True
        else:
            return False
        
    @classmethod
    def delete_door(cls, door:Door):
        execute(f'DELETE FROM tuer WHERE id = \'{door.id}\'')
