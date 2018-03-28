import sqlite3


def dict2Str1(dict):
    field_list = []
    for key,val in dict.items():
        statment = '%s %s' % (key,val)
        field_list.append(statment)
    return ','.join(field_list)

def dict2Str2(dict):
    key_list = []
    value_list = []
    for key,val in dict.items():
        key_list.append('%s' % key)
        if type(val) is str:
            value_list.append("'%s'" % val)
        else:
            value_list.append('%s' % val)
    return (','.join(key_list), ','.join(value_list))

class Database(object):
    def __init__(self, env):
        self.env = env
        self.conn = sqlite3.connect(self.env.config.gate.data_file)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
    
    def execute(self, sql):
        return self.cursor.execute(sql)

    def createTable(self, table_name, field_dict):
        field_expression = dict2Str1(field_dict)
        sql = 'create table %s (%s)' % (table_name, field_expression)
        self.cursor.execute(sql)

    def insert(self, table_name, field_dict):
        (field_name, field_value) = dict2Str2(field_dict)
        sql = 'insert into %s (%s) values (%s)' % (table_name, field_name, field_value)
        self.cursor.execute(sql)
        self.conn.commit()

    def query(self, table_name, field_dict):
        (field_name, _) = dict2Str2(field_dict)
        sql = 'select %s from %s' % (field_name, table_name)
        result = self.cursor.execute(sql)
        return result.fetchall()


if __name__ == '__main__':
    from common.environment import Env
    env = Env()
    db = Database(env)
    sql = 'select rowid,last from eos_usdt where rowid > 30'
    result = db.execute(sql)
    data = result.fetchall()
    print(data)
    pair = data[-1]
    print(pair)
    row_id = pair[0]
    print(row_id)
    
