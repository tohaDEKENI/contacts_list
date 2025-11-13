from tkinter import *
from .database import Database
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk

class Ui:
    def __init__(self,title="contacts_list"):
        self.db = Database()
        self.root = Tk()
        self.root.configure(background="lightgray")
        self.root.geometry("1000x600")
        self.root.resizable(False,False)
        self.root.title(title)

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading",font=("Arial",13,"bold"))

        self.image = Image.open("contacts_list/assets/contact-mail.png").resize((50,50))
        self.img = ImageTk.PhotoImage(self.image)

        self.image_label = ttk.Label(self.root,image=self.img,background="lightblue")
        self.image_label.place(x=0,y=0)

        self.form_title = ttk.Label(self.root,text="Create a new contacts",foreground="#2C3930",font=("Arial",25),background="lightgray")
        self.form_title.pack()

        self.label_lastname = ttk.Label(self.root,text="Lastname:",font=("Arial",13,"bold"))
        self.label_lastname.place(x=10,y=60)
        self.lastname_entry = ttk.Entry(self.root,width=50,background="red")
        self.lastname_entry.place(x=100,y=60)

        self.label_firstname = ttk.Label(self.root,text="Firstname:",font=("Arial",13,"bold"))
        self.label_firstname.place(x=500,y=60)
        self.firstname_entry = ttk.Entry(self.root,width=50)
        self.firstname_entry.place(x=600,y=60)

        self.label_email = ttk.Label(self.root,text="Email:",font=("Arial",13,"bold"))
        self.label_email.place(x=10,y=100)
        self.email_entry = ttk.Entry(self.root,width=50,background="red")
        self.email_entry.place(x=100,y=100)

        self.label_contact = ttk.Label(self.root,text="Contact:",font=("Arial",13,"bold"))
        self.label_contact.place(x=500,y=100)
        self.contact_enrty = ttk.Entry(self.root,width=50)
        self.contact_enrty.place(x=600,y=100)

        self.create_btn = ttk.Button(self.root,text="Create contact",width=20,command=self.create_new_contact)
        self.create_btn.place(x=600,y=140)

        self.create_btn = ttk.Button(self.root,text="Reset",width=20)
        self.create_btn.place(x=780,y=140)

        self.tree_columns = ("Id","Last name","First name","Email","Contact")

        self.treeview = ttk.Treeview(self.root,columns=self.tree_columns,show="headings")
        self.treeview.place(x=10,y=200,width=900,height=350)

        self.delete_btn = ttk.Button(self.root,text="DELETE",command=self.delete_contact)
        self.delete_btn.place(x=920,y=200)

        self.modify_btn = ttk.Button(self.root, text="MODIFY",command=self.modify_contact)
        self.modify_btn.place(x=920, y=240)

        for col in self.tree_columns:
            self.treeview.heading(col,text=col)

        for col in self.tree_columns:
            self.treeview.column(col,anchor="center")

        self.treeview.column("Id",width=10)

        self.get_contact()


    def create_new_contact(self):
        lastname = self.lastname_entry.get()
        firstname = self.firstname_entry.get()
        email = self.email_entry.get()
        contact = self.contact_enrty.get()

        if lastname == "":
            messagebox.showinfo("Missing Information", message="The last name field is empty.")
        elif firstname == "":
            messagebox.showinfo("Missing Information", message="The first name field is empty.")
        elif email == "":
            messagebox.showinfo("Missing Information", message="The email field is empty.")
        elif contact == "":
            messagebox.showinfo("Missing Information", message="The contact field is empty.")
        else:
            self.db.create_contact(lastname,firstname,email,contact)
            messagebox.showinfo("Success", message="The contact has been successfully created!")
            self.lastname_entry.delete(0,END)
            self.firstname_entry.delete(0,END)
            self.email_entry.delete(0,END)
            self.contact_enrty.delete(0,END)
            self.get_contact()
        
    def get_contact(self):
        contacts = self.db.get_contacts()
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for cont in contacts:
            self.treeview.insert("",END,values=cont)

    def delete_contact(self):
        selection = self.treeview.selection()

        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return

        response = messagebox.askquestion("Question", "Are you sure you want to delete this contact?")

        if response == "yes":
            for item in selection:
                values = self.treeview.item(item, "values")
                self.db.delete_contact(values[0])
                self.treeview.delete(item)

            messagebox.showinfo("Success", "Contact(s) deleted successfully.")
    
    def modify_contact(self):
        selection = self.treeview.selection()

        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to modify.")
            return

        popup = Toplevel(self.root)
        popup.title("Modify Contact")
        popup.geometry("430x300")
        popup.resizable(False, False)

        label_lastname = ttk.Label(popup, text="Lastname:", font=("Arial", 13, "bold"))
        label_lastname.place(x=10, y=60)
        lastname_entry = ttk.Entry(popup, width=50)
        lastname_entry.place(x=120, y=60)

        label_firstname = ttk.Label(popup, text="Firstname:", font=("Arial", 13, "bold"))
        label_firstname.place(x=10, y=100)
        firstname_entry = ttk.Entry(popup, width=50)
        firstname_entry.place(x=120, y=100)

        label_email = ttk.Label(popup, text="Email:", font=("Arial", 13, "bold"))
        label_email.place(x=10, y=160)
        email_entry = ttk.Entry(popup, width=50)
        email_entry.place(x=120, y=160)

        label_contact = ttk.Label(popup, text="Contact:", font=("Arial", 13, "bold"))
        label_contact.place(x=10, y=200)
        contact_entry = ttk.Entry(popup, width=50)
        contact_entry.place(x=120, y=200)

        item = selection[0]
        values = self.treeview.item(item, "values")
        contact_id = values[0]

        lastname_entry.insert(0, values[1])
        firstname_entry.insert(0, values[2])
        email_entry.insert(0, values[3])
        contact_entry.insert(0, values[4])

        def save_contact():
            lastname = lastname_entry.get().strip()
            firstname = firstname_entry.get().strip()
            email = email_entry.get().strip()
            contact = contact_entry.get().strip()

            if not lastname or not firstname or not email or not contact:
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return

            self.db.modify_contact(contact_id, lastname, firstname, email, contact)

            if hasattr(self, "refresh_tree"):
                self.refresh_tree()

            messagebox.showinfo("Success", f"Contact '{firstname} {lastname}' updated successfully.")
            popup.destroy()
            self.get_contact()

        def reset_fields():
            lastname_entry.delete(0, END)
            firstname_entry.delete(0, END)
            email_entry.delete(0, END)
            contact_entry.delete(0, END)

        ttk.Button(popup, text="Modify Contact", width=20, command=save_contact).place(x=100, y=240)
        ttk.Button(popup, text="Reset", width=20, command=reset_fields).place(x=260, y=240)            

    def run(self):
        self.root.mainloop()