from utils.dsql.dsql import execute, query
from . transponder import Transponder, TransponderOperations
from . groups import Group
from . door import Door
import uuid

class User:

    def __init__(self, user_no):
        self.id = uuid.uuid4()
        self.user_no = user_no
        
        self.firstname = None
        self.lastname = None
        self.email = None
        self.transponder = None

        # Erstelle oder lade das User objekt
        if not UserOperations.is_user_exists(user_no):
            self.__create_database_entry()
        else:
            self.id = query(f'SELECT id FROM nutzer WHERE nutzer_no = \'{user_no}\' LIMIT 1')[0][0]
            self.firstname = query(f'SELECT vorname FROM nutzer WHERE nutzer_no = \'{user_no}\' LIMIT 1')[0][0]
            self.lastname = query(f'SELECT nachname FROM nutzer WHERE nutzer_no = \'{user_no}\' LIMIT 1')[0][0]
            self.email = query(f'SELECT email FROM nutzer WHERE nutzer_no = \'{user_no}\' LIMIT 1')[0][0]
            self.transponder = query(f'SELECT transponder_id FROM nutzer WHERE nutzer_no = \'{user_no}\' LIMIT 1')[0][0]


    def __create_database_entry(self):
        execute(f'INSERT INTO nutzer(id, nutzer_no) VALUES (\'{self.id}\', \'{self.user_no}\')')
    
    def set_name(self, firstname = None, lastname = None):
        if firstname is not None:
            self.firstname = firstname
            execute(f'UPDATE nutzer SET vorname = \'{firstname}\' WHERE id = \'{self.id}\'')
        if lastname is not None:
            self.lastname = lastname
            execute(f'UPDATE nutzer SET nachname = \'{lastname}\' WHERE id = \'{self.id}\'')
    
    def set_email(self, email):
        self.email = email
        execute(f'UPDATE nutzer SET email = \'{email}\' WHERE id = \'{self.id}\'')

class UserOperations:

    @classmethod
    def get_user(cls, vorname, nachname, email):
        user = User(vorname, nachname, email)
        user.id = query(f'SELECT id FROM nutzer WHERE vorname = \'{vorname}\' AND nachname = \'{nachname}\' AND email = \'{email}\'')[0][0]
        if TransponderOperations.get_transponder_from_user(user.id) is not None:
            user.transponder = TransponderOperations.get_transponder_from_user(user.id).id
        else: user.transponder = None
        return user
    
    @classmethod
    def is_user_exists(cls, user_no):
        if query(f'SELECT COUNT(id) FROM nutzer WHERE nutzer_no = \'{user_no}\'')[0][0] > 0:
            return True
        else:
            return False
        
    @classmethod
    def get_user_count(cls):
        return query('SELECT user_count FROM user_operations')[0][0]
    
    @classmethod
    def assign_transponder(cls, user:User, transponder:Transponder):
        
        # Da ein Transponder nur eine 1:1 Kardinalität hat, muss der alte besitzer wieder entfernt werden und wieder entsperrt werden
        potential_owner = query(f'SELECT n.id FROM transponder t INNER JOIN nutzer n ON t.id = n.transponder_id WHERE t.id = \'{transponder.id}\'')
        if len(potential_owner) > 0:
            execute(f'UPDATE nutzer SET transponder_id = NULL WHERE id = \'{potential_owner[0][0]}\'')
            TransponderOperations.write_log(transponder.id, f'MOVED - NEW_OWNER_{user.user_no}')
        execute(f'UPDATE nutzer SET transponder_id = \'{transponder.id}\' WHERE id = \'{user.id}\'')
        TransponderOperations.write_log(transponder.id, f'MOVED - RECIEVED_{user.user_no}')
        execute(f'UPDATE transponder SET gesperrt = 0 WHERE id = \'{transponder.id}\'')
        TransponderOperations.write_log(transponder.id, f'UNLOCKED - TRANSFER')

    @classmethod
    def delete_user(cls, user:User):
        # Falls ein nutzer gelöscht wird, welcher noch einen Transponder hat, so wird der Transponder deaktiviert!
        if UserOperations.has_transponder(user):
            transponder = Transponder(user.transponder)
            TransponderOperations.lock_transponder(transponder, 'LOCKED - ACCOUNT DELETION')
        execute(f'DELETE FROM nutzer WHERE id = \'{user.id}\'')

    @classmethod
    def has_transponder(cls, user:User):
        if user.transponder:
            return True
        return False
    
    @classmethod
    def get_groups(cls, user:User):
        group_list_result_set = query(f'SELECT gruppen_id FROM nutzer_gruppen ng INNER JOIN nutzer n ON n.id = ng.nutzer_id WHERE n.id = \'{user.id}\'')
        print(group_list_result_set)

    @classmethod
    def is_in_group(cls, user:User, group:Group):
        in_group = query(f'SELECT COUNT(*) FROM nutzer_gruppen ng INNER JOIN nutzer n ON n.id = ng.nutzer_id INNER JOIN gruppe g ON g.id = ng.gruppen_id WHERE n.nutzer_no = \'{user.user_no}\' AND g.group_no = \'{group.group_no}\'')[0][0]
        if in_group > 0:
            return True
        else:
            return False
        

    @classmethod
    def assign_to_group(cls, user:User, group:Group):
        execute(f'INSERT INTO nutzer_gruppen(nutzer_id, gruppen_id) VALUES (\'{user.id}\', \'{group.id}\')')

    @classmethod
    def remove_from_group(cls, user:User, group:Group):
        execute(f'DELETE FROM nutzer_gruppen WHERE nutzer_id = \'{user.id}\' AND gruppen_id = \'{group.id}\'')

    @classmethod
    def has_door_access(cls, user:User, door:Door):
        has_access = query(f'SELECT COUNT(*) FROM nutzer_tuer_zugriff ntz INNER JOIN nutzer n ON n.id = ntz.nutzer_id INNER JOIN tuer t ON t.id = ntz.tuer_id WHERE n.nutzer_no = \'{user.user_no}\' AND t.id = \'{door.id}\'')[0][0]
        if has_access > 0:
            return True
        else:
            return False

    @classmethod
    def add_door_access(cls, user:User, door:Door):
        execute(f'INSERT INTO nutzer_tuer_zugriff(tuer_id, nutzer_id, erlaubt) VALUES (\'{door.id}\', \'{user.id}\', \'0\')')

    @classmethod
    def remove_door_access(cls, user:User, door:Door):
        execute(f'DELETE FROM nutzer_tuer_zugriff WHERE tuer_id = \'{door.id}\' AND nutzer_id = \'{user.id}\'')