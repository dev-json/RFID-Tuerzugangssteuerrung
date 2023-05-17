from utils.dsql.dsql import execute

class DoorLogOperational:
    
    @classmethod
    def write_log_entry(cls, door_id, user_id, action):
        execute(f'INSERT INTO tuer_zugriff_historie(tuer_id, nutzer_id, information) VALUES (\'{door_id}\', \'{user_id}\', \'{action}\')')