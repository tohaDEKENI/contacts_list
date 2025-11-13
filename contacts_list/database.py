import sqlite3

class Database:
    def __init__(self,db_name="contacts_list/database/contacts.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    # Create the contacts table in database
    def create_table(self):
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS contacts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lastname TEXT NOT NULL,
                    firstname TEXT NOT NULL,
                    email TEXT NOT NULL,
                    contact TEXT NOT NULL
                )
            """
        )
        self.conn.commit()
    
    # Create a new contact to the database
    def create_contact(self,lastname,firstname,email,contact):
        self.cursor.execute(
            """
                INSERT INTO contacts (lastname,firstname,email,contact)
                VALUES(?,?,?,?)
            """,
            (lastname,firstname,email,contact)
        )
        self.conn.commit()
    
    # Retrieve all contacts from the database
    def get_contacts(self):
        self.cursor.execute("SELECT * FROM contacts")
        resultat = self.cursor.fetchall()
        return resultat
    
    # Remove a contact from the database by its unique UUID identifier
    def delete_contact(self,id):
        self.cursor.execute("DELETE FROM contacts WHERE id = ?",(id,))
        self.conn.commit()

    def modify_contact(self,id,lastname,firstname,email,contact):
        self.cursor.execute(
            """UPDATE contacts SET lastname = ?,firstname = ?,email = ?,contact = ? WHERE id = ?""",
                (lastname,firstname,email,contact,id)
        )
        self.conn.commit()


#  py .\contact_list\database.py