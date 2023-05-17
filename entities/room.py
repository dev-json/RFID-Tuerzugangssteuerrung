from utils.dsql.dsql import execute, query

from .building import Building

class Room:
    
    def __init__(self, id):
        self.id = id
        self.description = None
        self.building = None

        if not RoomOperational.is_room_exists(self.id):
            self.__create_database_entry()
        else:
            self.description = query(f'SELECT beschreibung FROM raum WHERE id = \'{self.id}\'')[0][0]

    def __create_database_entry(self):
        execute(f'INSERT INTO raum(id) VALUES (\'{self.id}\')')

    def set_description(self, description = None):
        if description is not None:
            self.description = description
            execute(f'UPDATE raum SET beschreibung = \'{description}\' WHERE id = \'{self.id}\'')
    
    def set_building(self, building:Building = None):
        if building is not None:
            self.building = building.id
            execute(f'UPDATE raum SET gebaeude_id = \'{building.id}\' WHERE id = \'{self.id}\'')
class RoomOperational:
    
    @classmethod
    def is_room_exists(cls, room_id):
        if query(f'SELECT COUNT(id) FROM raum WHERE id = \'{room_id}\'')[0][0] > 0:
            return True
        else:
            return False
        
    @classmethod
    def delete_room(cls, room:Room):
        execute(f'DELETE FROM raum WHERE id = \'{room.id}\'')
        