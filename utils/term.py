import os
import helper
import constants

from cmd import Cmd
from db import Database
from helper import generate_xml

class Terminal(Cmd):

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.prompt = self.db.current_table + '> '

    def help_display_table(self):
        print("[?] Displays the entries in the current table")
        print("[?] USAGE: display_table\n")
    
    def do_display_table(self, args):
        self.db.display_table()     

    def help_add(self):
        print("[?] Adds a user into current table.")
        print("[?] USAGE: add 'NAME' | 'USERNAME' | 'EMAIL' | 'SMB_PATH'\n")

    def do_add(self, args):
        user_info = args.split('|')

        if len(user_info) == self.db.num_of_columns - 1:
            self.db.insert_user(user_info)
            return

        print(f"[-] User was not added, {len(user_info)} args given {self.db.num_of_columns - 1} needed.")
        print("[?] USAGE: add 'NAME' | 'USERNAME' | 'EMAIL' | 'SMB_PATH'\n")
    

    def help_delete(self):
        print("[?] Deletes user from the current table.")
        print("[?] USAGE: delete 'USERNAME'\n")

    def do_delete(self, args):
        username = args.split(" ")[0]
        
        self.db.delete_user(username)

    def help_wipe(self):
        print("[?] Wipes the current table.")
        print("[?] USAGE: wipe \n")
    
    def do_wipe(self, args):
        self.db.truncate_table()

    def help_find(self):
        print("[?] Searches current table for the specified user and displays entry if found.")
        print("[?] USAGE: find 'USERNAME'\n")

    def do_find(self, args):
        username = args.split(' ')[0]

        if self.db.user_exists(username, True):
            return

    def help_switch(self):
        print("[?] Switches the current table to the one specified, if it exists within the database.")
        print("[?] USAGE: switch 'TABLE_NAME'\n")

    def do_switch(self, args):
        table_name = args.split(' ')[0]

        if self.db.switch_table(table_name): 
            self.prompt = self.db.current_table + "> "

    def help_create_table(self):
        print("[?] Creates a new table.")
        print("[?] USAGE: create_table 'TABLE_NAME' \n")

    def do_create_table(self, args):
        if len(args.split(" ")) < 1:
            print("[?] USAGE: create_table 'TABLE_NAME'")
            return
        
        self.db.create_table(args.split(' ')[0])
        self.prompt = self.db.current_table + "> "

    def help_tables(self):
        print("[?] Displays all the tables within the database.")
        print("[?] USAGE: tables\n")

    def do_tables(self, args): 
        self.db.get_tables()

    def help_load(self):
        print("[?] Loads users from specified csv file into the current table.")
        print("[?] USAGE: load 'CSV_FILE'\n")

    def do_load(self, args):
        filename = os.path.realpath(args)
        
        self.db.load_csv(filename)

    def help_generate_book(self):
        print("[?] Generates an address books xml file for the current table.")
        print("[?] USAGE: generate_book <OPTIONAL_FILENAME>\n")

    def do_generate_book(self, filename=""):
        if filename == "":
            filename = self.db.current_table
        
        user_data = self.db.get_all_users()

        generate_xml(user_data, filename)

    def help_exit(self):
        print("[?] Exits the application...")
        print("[?] USAGE: exit\n")

    def do_exit(self, args):
        print("Bye!")
        return True
    
    def emptyline(self):
        return