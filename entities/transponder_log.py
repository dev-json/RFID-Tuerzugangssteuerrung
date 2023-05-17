from utils.dsql.dsql import execute

class TransponderLogOperational:
    
    @classmethod
    def write_log_entry(cls, id, aktion):
        execute(f'INSERT INTO transponder_historie(transponder_id, aktion) VALUES (\'{id}\', \'{aktion}\')')