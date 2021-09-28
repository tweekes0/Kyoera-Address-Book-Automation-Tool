import constants
import csv
import sqlite3

from sqlite3 import Error

class Database: 

    def __init__(self, db_name=constants.DEFAULT_DATABASE):
        self.db_connection = sqlite3.connect(db_name)
        self.cursor = self.db_connection.cursor()
        self.current_table = constants.DEFAULT_TABLE

        self.create_table(constants.DEFAULT_TABLE)    
        self.num_of_columns = self.get_column_count()        

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.db_connection.close()

    def commit(self):
        return self.db_connection.commit()

    def user_exists(self, username, show_info=False):
        sql = f''' SELECT * FROM {self.current_table} 
                   WHERE username = ? ''' 

        try: 
            self.cursor.execute(sql, (username,))
            row = self.cursor.fetchone()
        except Error as e:
            print(f"[-] {e}")
            return 

        if row == None:
            return False

        if show_info:
            print(f'{"ID":^5} | {"NAME":^25} | {"USERNAME":^15} | {"EMAIL":^20} | {"SMB_PATH":^15}')
            print(rf'{row[0]:^5} | {row[1]:^25} | {row[2]:^15} | {row[3]:^20} | {row[4]:^15}')
            print()
            
        return True

    def insert_user(self, user_info):
        user_info = [info.strip() for info in user_info]

        sql = f''' INSERT INTO '{self.current_table}' (name, username, email, smb_path)
                   VALUES (?, ?, ?, ?)'''
        
        if user_info[0] == "" or user_info[1] == "":
            print("[-] Name and username cannot be blank.\n")
            return

        if self.user_exists(user_info[1]):
            print(f"[-] User: '{user_info[1]}' already exists.\n")
            return
        
        try: 
            self.cursor.execute(sql, user_info)
            print(f"[+] {user_info[0]} added successfully.")
            self.commit()
        except Error as e:
            print(f"[-] {e}\n")
            return 
    
    def get_all_users(self):
        sql = f''' SELECT * FROM '{self.current_table}' '''

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Error as e:
            print(f"[-] {e}\n")
            return

    def delete_user(self, username):
        sql = f''' DELETE FROM {self.current_table} 
                   WHERE username = ? '''
        
        if username == "":
            print(f"[-] Please enter a username.\n")
            return  

        if not self.user_exists(username):
            print(f"[-] '{username}' does not exist.")
            return
        
        try: 
            self.cursor.execute(sql, (username,))
            print(f"[+] '{username}' deleted successfully.\n")
            self.commit()
        except Error as e:
            print(f"[-] {e}\n")
            return

    def table_exists(self, table_name):
        sql = f''' SELECT count(name) FROM sqlite_master 
                   WHERE type='table' and name='{table_name}' '''
                
        self.cursor.execute(sql)
        
        if self.cursor.fetchone()[0]:
            return True

        return False

    def create_table(self, table_name):
        sql = f''' CREATE TABLE IF NOT EXISTS {table_name}(
                   id integer PRIMARY KEY AUTOINCREMENT,
                   name text NOT NULL,
                   username text NOT NULL,
                   email text NOT NULL,
                   smb_path text NOT NULL
            ); '''
        
        if self.table_exists(table_name):
            return
        
        try: 
            self.cursor.execute(sql)
            print(f"[+] '{table_name}' created successfully.\n")
            self.current_table = table_name
        except Error:
            print(f"[-] Cannot create table '{table_name}' ")
            print(f"[-] Table name cannot spaces or special characters.")
    
    def drop_table(self, table_name):
        sql = f''' DROP TABLE {table_name} '''

        if table_name == constants.DEFAULT_TABLE or table_name == 'sqlite_sequence':
            print("[-] You cannot delete this table.\n")
            return
        
        try: 
            self.cursor.execute(sql) 
            self.commit()
        except Error as e:
            print(f"[-] {e}\n")

    def truncate_table(self):
        sql = f''' DELETE FROM {self.current_table} '''

        try:
            self.cursor.execute(sql)
            self.commit()
            print(f"[+] '{self.current_table}' wiped.\n")
        except Error as e:
            print(f"[-] {e}\n")
        
    def switch_table(self, table_name=constants.DEFAULT_TABLE):
        sql = f''' SELECT name FROM sqlite_master 
                   WHERE type = 'table' and name != 'sqlite_sequence' 
                   ORDER BY name '''

        try: 
            self.cursor.execute(sql)
            tables = self.cursor.fetchall()

            if (table_name,) in tables:
                self.current_table = table_name

            return True
        except Error as e:
            print(f"[-] {e}\n")
            return False

    def display_table(self): 
        sql = f''' SELECT * FROM {self.current_table} '''

        try: 
            self.cursor.execute(sql)
            users = self.cursor.fetchall()
        except Error as e:
            print(f"[-] {e}\n")
            return 

        if len(users) == 0:
            print(f"[-] '{self.current_table}' is empty\n")
            return
        
        print(f'{"ID":^5} | {"NAME":^25} | {"USERNAME":^15} | {"EMAIL":^30} | {"SMB_PATH":^15}')
        for user in users:
            print(rf'{user[0]:^5} | {user[1]:^25} | {user[2]:^15} | {user[3]:^30} | {user[4]:^15}')
        
        print()

    def get_tables(self):
        sql = f''' SELECT name FROM sqlite_master
                   WHERE type = 'table' AND  name != 'sqlite_sequence' '''
        
        try:   
            self.cursor.execute(sql) 
            tables = self.cursor.fetchall()
            print(f'\n{"TABLE_NAME":^25} | {"# OF RECORDS":^5}')
            for table in tables:
                second_sql = f''' SELECT COUNT(*) FROM {table[0]} '''
                self.cursor.execute(second_sql)
                count = self.cursor.fetchone()[0]
                print(f'{table[0]:^25} | {count:^9}')
            print()        
        except Error as e:
            print(f"[-] {e}\n")
            return

    def load_csv(self, filename):
        try: 
            with open(filename) as users_file: 
                reader = csv.DictReader(users_file)

                for row in reader:
                    self.insert_user((row["NAME"].title(), row["USERNAME"], row["EMAIL"], row["SMB_PATH"]))
                print()
        except FileNotFoundError:    
            print(rf'[-] {filename} not found')
        except KeyError:
            print("[-] File must be a CSV, Check csv column headers.")
            print("[-] Headers should be NAME,USERNAME,EMAIL,SMB_PATH\n")

    def get_column_count(self):
        sql = f''' PRAGMA table_info({self.current_table}) '''

        try: 
            self.cursor.execute(sql) 
            col_count = len(self.cursor.fetchall())

            return col_count
        except Error as e:
            print(f"[-] {e}\n")
            return
