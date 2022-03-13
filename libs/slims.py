import mysql.connector
from mysql.connector import Error

class Slims:
    
    def __init__(self, host, port, username, password, dbname):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=dbname
        )
        
        self.cursor = self.connection.cursor()
        
    def find(self, memberId, memberTypeId):
        sql = "SELECT * FROM member WHERE member_id = %s AND member_type_id = %s"
        
        self.cursor.execute(sql, (
            memberId,
            memberTypeId
        ))
        
        return self.cursor.fetchone()
    
        
    def insert(self, member):
        sql = "INSERT INTO member (member_id, member_name, gender, member_type_id, member_email, member_address, inst_name, pin, member_phone, member_fax, member_since_date, register_date, expire_date, birth_date, member_notes, mpasswd, input_date, last_update) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"

        self.cursor.execute(sql, (
            member['member_id'],
            member['member_name'],
            member['gender'],
            member['member_type_id'],
            member['member_email'],
            member['member_address'],
            member['inst_name'],
            member['pin'],
            member['member_phone'],
            member['member_fax'],
            member['member_since_date'],
            member['register_date'],
            member['expire_date'],
            member['birth_date'],
            member['member_notes'],
            member['mpasswd'],
            member['input_date'],
            member['last_update'],
        ))
        
        
    def update(self, member):
        sql = "UPDATE member SET member_name = %s, is_pending = 0, gender = %s, member_email = %s, member_address = %s, inst_name = %s, member_phone = %s, member_fax = %s WHERE member_id = %s"
        
        self.cursor.execute(sql, (
            member['member_name'],
            member['gender'],
            member['member_email'],
            member['member_address'],
            member['inst_name'],
            member['member_phone'],
            member['member_fax'],
            member['member_id'],
            
        ))
    
    def deactivate(self, memberTypeId):
        sql = "UPDATE member SET is_pending = 1, expire_date = '2000-05-02' WHERE member_type_id = %s"
        
        self.cursor.execute(sql, (
            memberTypeId,
        ))
        
        self.commit()
        
    def commit(self):
        self.connection.commit()