from utils.dsql.dsql import execute, query
from . transponder_log import TransponderLogOperational
import uuid

class Transponder:
    def __init__(self, id = None):
        if id is None:
          self.id = uuid.uuid4()
          self.is_locked = 0
        else:
          self.id = id
        if not TransponderOperations.is_transponder_exists(self.id):
            self.__create_database_entry()
            TransponderOperations.write_log(id, 'CREATED')
        else:
            self.is_locked = query(f'SELECT gesperrt FROM transponder WHERE id = \'{self.id}\'')[0][0]

    def __create_database_entry(self):
        execute(f'INSERT INTO transponder(id) VALUES (\'{self.id}\')')

class TransponderOperations:

    @classmethod
    def lock_transponder(cls, transponder:Transponder, custom_message = None):
        if custom_message is None:
            custom_message = 'LOCKED'
        execute(f'UPDATE transponder SET gesperrt = 1 WHERE id = \'{transponder.id}\'')
        TransponderOperations.write_log(transponder.id, custom_message)
        transponder.is_locked = 1
    
    @classmethod
    def unlock_transponder(cls, transponder:Transponder, custom_message):
        if custom_message is None:
            custom_message = 'UNLOCKED'
        execute(f'UPDATE transponder SET gesperrt = 0 WHERE id = \'{transponder.id}\'')
        TransponderOperations.write_log(transponder.id, custom_message)
        transponder.is_locked = 0

    @classmethod
    def is_transponder_exists(cls, id):
        result = query(f'SELECT COUNT(id) FROM transponder WHERE id = \'{id}\'')
        # Prüfen ob result
        if len(result) > 0:
            # prüfen, ob count > 0
            if result[0][0] > 0:
                return True
            else:
                return False
    
    @classmethod
    def get_transponder_from_user(cls, id):
        transponder_id = query(f'SELECT transponder_id FROM nutzer n WHERE n.id = \'{id}\'')
        if len(transponder_id) > 0:
            return Transponder(transponder_id[0][0])
        else:
            return None
    
    @classmethod
    def get_transponder(cls, id):
        transponder_id = query(f'SELECT id, gesperrt FROM transponder t WHERE t.id = \'{id}\'')[0]
        if transponder_id:
            return Transponder(transponder_id[0])
        else:
            return None

    @classmethod
    def write_log(cls, transponder, aktion):
        TransponderLogOperational.write_log_entry(transponder, aktion)

    @classmethod
    def is_transponder_locked(cls, transponder:Transponder):
        if transponder.is_locked == 1:
            return True
        else: 
            return False

         
