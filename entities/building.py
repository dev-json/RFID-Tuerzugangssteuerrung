from utils.dsql.dsql import execute, query

class Building:
    
    def __init__(self, id):
        self.id = id
        self.description = None
        if not BuildingOperational.is_building_exists(self.id):
            self.__create_database_entry()
        else:
            self.description = query(f'SELECT beschreibung FROM gebaeude WHERE id = \'{self.id}\'')[0][0]

    def __create_database_entry(self):
        execute(f'INSERT INTO gebaeude(id) VALUES (\'{self.id}\')')

    def set_description(self, description = None):
        if description is not None:
            self.description = description
            execute(f'UPDATE gebaeude SET beschreibung = \'{description}\' WHERE id = \'{self.id}\'')

class BuildingOperational:
    
    @classmethod
    def is_building_exists(cls, building_id):
        if query(f'SELECT COUNT(id) FROM gebaeude WHERE id = \'{building_id}\'')[0][0] > 0:
            return True
        else:
            return False
        
    @classmethod
    def delete_building(cls, building:Building):
        execute(f'DELETE FROM gebaeude WHERE id = \'{building.id}\'')
        