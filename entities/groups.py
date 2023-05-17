from utils.dsql.dsql import execute, query
import uuid

class Group:

    def __init__(self, group_no):
        self.id = uuid.uuid4()
        self.group_no = group_no
        self.name = None

        # Erstelle oder lade das Gruppen objekt
        if not GroupOperations.is_group_exists(group_no):
            self.__create_database_entry()
        else:
            self.id = query(f'SELECT id FROM gruppe WHERE group_no = \'{group_no}\' LIMIT 1')[0][0]
            self.name = query(f'SELECT name FROM gruppe WHERE group_no = \'{group_no}\' LIMIT 1')[0][0]

    def __create_database_entry(self):
        execute(f'INSERT INTO gruppe(id, group_no) VALUES (\'{self.id}\', \'{self.group_no}\')')
    
    def set_name(self, name):
        self.name = name
        execute(f'UPDATE gruppe SET name = \'{name}\' WHERE id = \'{self.id}\'')
        

class GroupOperations:
    
    @classmethod
    def is_group_exists(cls, group_no):
        if query(f'SELECT COUNT(id) FROM gruppe WHERE group_no = \'{group_no}\'')[0][0] > 0:
            return True
        else:
            return False

    @classmethod
    def delete_group(cls, group:Group):
        execute(f'DELETE FROM gruppe WHERE id = \'{group.id}\'')

        