import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk, Toplevel


def insert_employee(employee_id, name, emp_location, phone_number):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="assetmgdb"
    )
    cursor = connection.cursor()
    try:
        cursor.execute('''
                       INSERT INTO employees (employee_id, name, emp_location, phone_number)
                        VALUES (%s, %s, %s, %s)
                       ''', (employee_id, name, emp_location, phone_number))
        print(employee_id, name, emp_location, phone_number)
        connection.commit()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        connection.close()


def insert_asset(asset_id, asset_name, asset_type, purchase_date, location, assigned_emp_id, notes):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="assetmgdb"
    )
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO assets (asset_id,asset_name, asset_type,purchase_date, location, assigned_emp_id, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (asset_id, asset_name, asset_type, purchase_date, location, assigned_emp_id, notes))

    connection.commit()
    connection.close()


def assign_asset(asset_id, employee_id):
    connection = mysql.connector.connect(
        host="localhost",
        username="root",
        password="1234",
        database="assetmgdb"
    )
    cursor = connection.cursor()

    cursor.execute('''UPDATE assets SET assigned_emp_id = %s WHERE asset_id = %s''',
                   (employee_id, asset_id))

    select_asset_query = "SELECT asset_name FROM assets WHERE asset_id = %s"
    cursor.execute(select_asset_query, (asset_id,))
    asset_name = cursor.fetchone()[0]

    select_employee_query = "SELECT name FROM employees WHERE employee_id = %s"
    cursor.execute(select_employee_query, (employee_id,))
    name = cursor.fetchone()[0]

    insert_query = '''
    INSERT INTO assigned_values (asset_id, employee_id, asset_name, name)
    VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(insert_query, (asset_id, employee_id, asset_name, name))

    connection.commit()
    cursor.close()


def update_asset(asset_id, new_asset_name, new_asset_type, new_purchase_date, new_location, new_assigned_emp_id, notes):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="assetmgdb"
    )
    cursor = connection.cursor()

    cursor.execute('''UPDATE assets SET asset_name = %s, asset_type = %s, purchase_date = %s, 
                    location = %s, assigned_emp_id = %s, notes = %s
                   WHERE asset_id = %s''', (
        new_asset_name, new_asset_type, new_purchase_date,
        new_location, new_assigned_emp_id, notes, asset_id
    ))

    connection.commit()
    cursor.close()
    connection.close()


def delete_asset(asset_id):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="assetmgdb"
    )
    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM assets
        WHERE asset_id = %s
    ''', (asset_id,))

    connection.commit()
    connection.close()


def view_asset(asset_id):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="assetmgdb"
    )
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM assets
        WHERE asset_id = %s
    ''', (asset_id,))

    asset = cursor.fetchone()
    connection.close()

    return asset


def view_employee(employee_id):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="assetmgdb"
    )

    cursor = connection.cursor()

    cursor.execute(
        '''select * from employees where employee_id = %s''', (employee_id,))

    employee = cursor.fetchall()
    print(employee)
    connection.close()


def check_employee_exists(employee_id):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="assetmgdb"
    )
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM employees WHERE employee_id = %s
    ''', (employee_id,))

    employee = cursor.fetchone()
    connection.close()

    return employee is not None


def check_asset_exists(asset_id):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="assetmgdb"
    )
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM assets WHERE asset_id = %s
    ''', (asset_id,))

    asset = cursor.fetchone()
    connection.close()

    return asset is not None


class AssetManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Asset Management System")

        self.create_tabs()

    def create_tabs(self):
        self.tabControl = ttk.Notebook(self.root)

        self.tab_insert_employee = ttk.Frame(self.tabControl)
        self.tab_insert_asset = ttk.Frame(self.tabControl)
        self.tab_update_asset = ttk.Frame(self.tabControl)
        self.tab_delete_asset = ttk.Frame(self.tabControl)
        self.tab_view_asset = ttk.Frame(self.tabControl)
        self.tab_assign_asset = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_insert_employee, text='Insert Employee')
        self.tabControl.add(self.tab_insert_asset, text='Insert Asset')
        self.tabControl.add(self.tab_update_asset, text='Update Asset')
        self.tabControl.add(self.tab_delete_asset, text='Delete Asset')
        self.tabControl.add(self.tab_view_asset, text='View Asset')
        self.tabControl.add(self.tab_assign_asset, text='Assign Asset')

        self.tabControl.pack(expand=1, fill="both")

        self.create_insert_employee_tab()
        self.create_insert_asset_tab()
        self.create_update_asset_tab()
        self.create_delete_asset_tab()
        self.create_view_asset_tab()
        self.create_assign_asset_tab()

    def create_insert_employee_tab(self):
        self.label_employee_id = tk.Label(
            self.tab_insert_employee, text="employee_id:")
        self.label_employee_id.grid(row=0, column=0)
        self.entry_employee_id = tk.Entry(self.tab_insert_employee)
        self.entry_employee_id.grid(row=0, column=1)

        self.label_name = tk.Label(self.tab_insert_employee, text="Name:")
        self.label_name.grid(row=1, column=0)
        self.entry_name = tk.Entry(self.tab_insert_employee)
        self.entry_name.grid(row=1, column=1)

        self.label_emp_location = tk.Label(
            self.tab_insert_employee, text="emp_location:")
        self.label_emp_location.grid(row=2, column=0)
        self.entry_emp_location = tk.Entry(self.tab_insert_employee)
        self.entry_emp_location.grid(row=2, column=1)

        self.label_phone_number = tk.Label(
            self.tab_insert_employee, text="phone_number:")
        self.label_phone_number.grid(row=3, column=0)
        self.entry_phone_number = tk.Entry(self.tab_insert_employee)
        self.entry_phone_number.grid(row=3, column=1)

        self.button_insert_employee = tk.Button(
            self.tab_insert_employee, text="Insert Employee", command=self.insert_employee)
        self.button_insert_employee.grid(row=4, columnspan=2)

    def create_insert_asset_tab(self):
        self.label_asset_id = tk.Label(
            self.tab_insert_asset, text="Asset_id:")
        self.label_asset_id.grid(row=0, column=0)
        self.entry_asset_id = tk.Entry(self.tab_insert_asset)
        self.entry_asset_id.grid(row=0, column=1)

        self.label_asset_name = tk.Label(
            self.tab_insert_asset, text="Asset_name:")
        self.label_asset_name.grid(row=1, column=0)
        self.entry_asset_name = tk.Entry(self.tab_insert_asset)
        self.entry_asset_name.grid(row=1, column=1)

        self.label_asset_type = tk.Label(
            self.tab_insert_asset, text="Asset Type:")
        self.label_asset_type.grid(row=2, column=0)
        self.entry_asset_type = tk.Entry(self.tab_insert_asset)
        self.entry_asset_type.grid(row=2, column=1)

        self.label_purchase_date = tk.Label(
            self.tab_insert_asset, text="Purchase Date:")
        self.label_purchase_date.grid(row=3, column=0)
        self.entry_purchase_date = tk.Entry(self.tab_insert_asset)
        self.entry_purchase_date.grid(row=3, column=1)

        self.label_location = tk.Label(
            self.tab_insert_asset, text="location:")
        self.label_location.grid(row=4, column=0)
        self.entry_location = tk.Entry(self.tab_insert_asset)
        self.entry_location.grid(row=4, column=1)

        self.label_assigned_emp_id = tk.Label(
            self.tab_insert_asset, text="assigned_emp_id:")
        self.label_assigned_emp_id.grid(row=5, column=0)
        self.entry_assigned_emp_id = tk.Entry(self.tab_insert_asset)
        self.entry_assigned_emp_id.grid(row=5, column=1)

        self.label_notes = tk.Label(
            self.tab_insert_asset, text="notes:")
        self.label_notes.grid(row=6, column=0)
        self.entry_notes = tk.Entry(self.tab_insert_asset)
        self.entry_notes.grid(row=6, column=1)

        self.button_insert_asset = tk.Button(
            self.tab_insert_asset, text="Insert Asset", command=self.insert_asset)
        self.button_insert_asset.grid(row=7, columnspan=2)

    def create_update_asset_tab(self):
        self.label_asset_id_update = tk.Label(
            self.tab_update_asset, text="Asset ID:")
        self.label_asset_id_update.grid(row=0, column=0)
        self.entry_asset_id_update = tk.Entry(self.tab_update_asset)
        self.entry_asset_id_update.grid(row=0, column=1)

        self.label_new_asset_name = tk.Label(
            self.tab_update_asset, text="New Asset Name:")
        self.label_new_asset_name.grid(row=1, column=0)
        self.entry_new_asset_name = tk.Entry(self.tab_update_asset)
        self.entry_new_asset_name.grid(row=1, column=1)

        self.label_new_asset_type = tk.Label(
            self.tab_update_asset, text="New Asset Type:")
        self.label_new_asset_type.grid(row=2, column=0)
        self.entry_new_asset_type = tk.Entry(self.tab_update_asset)
        self.entry_new_asset_type.grid(row=2, column=1)

        self.label_new_purchase_date = tk.Label(
            self.tab_update_asset, text="New Purchase Date:")
        self.label_new_purchase_date.grid(row=3, column=0)
        self.entry_new_purchase_date = tk.Entry(self.tab_update_asset)
        self.entry_new_purchase_date.grid(row=3, column=1)

        self.label_new_location = tk.Label(
            self.tab_update_asset, text="New location:")
        self.label_new_location.grid(row=4, column=0)
        self.entry_new_location = tk.Entry(self.tab_update_asset)
        self.entry_new_location.grid(row=4, column=1)

        self.label_new_assigned_emp_id = tk.Label(
            self.tab_update_asset, text="new_assigned emp id:")
        self.label_new_assigned_emp_id.grid(row=5, column=0)
        self.entry_new_assigned_emp_id = tk.Entry(self.tab_update_asset)
        self.entry_new_assigned_emp_id.grid(row=5, column=1)

        self.label_new_notes = tk.Label(
            self.tab_update_asset, text="New notes:")
        self.label_new_notes.grid(row=6, column=0)
        self.entry_new_notes = tk.Entry(self.tab_update_asset)
        self.entry_new_notes.grid(row=6, column=1)

        self.button_update_asset = tk.Button(
            self.tab_update_asset, text="Update Asset", command=self.update_asset)
        self.button_update_asset.grid(row=7, columnspan=2)

    def create_delete_asset_tab(self):
        self.label_asset_id_delete = tk.Label(
            self.tab_delete_asset, text="Asset ID:")
        self.label_asset_id_delete.grid(row=0, column=0)
        self.entry_asset_id_delete = tk.Entry(self.tab_delete_asset)
        self.entry_asset_id_delete.grid(row=0, column=1)

        self.button_delete_asset = tk.Button(
            self.tab_delete_asset, text="Delete Asset", command=self.delete_asset)
        self.button_delete_asset.grid(row=1, columnspan=2)

    def create_ui(self):
        self.button_view = tk.Button(
            self.root, text="View Values", command=self.create_view_asset_tab)
        self.button_view.pack()

    def create_view_asset_tab(self):
        self.label_asset_id = tk.Label(
            self.tab_view_asset, text="Asset_id:")
        self.label_asset_id.grid(row=0, column=0)
        self.entry_asset_id = tk.Entry(self.tab_view_asset)
        self.entry_asset_id.grid(row=0, column=1)

        self.button_view_asset = tk.Button(
            self.tab_view_asset, text="View Asset", command=self.view_asset)
        self.button_view_asset.grid(row=1, columnspan=2)

    def create_assign_asset_tab(self):
        self.label_asset_id_assign = tk.Label(
            self.tab_assign_asset, text="Asset ID:")
        self.label_asset_id_assign.grid(row=0, column=0)
        self.entry_asset_id_assign = tk.Entry(self.tab_assign_asset)
        self.entry_asset_id_assign.grid(row=0, column=1)

        self.label_employee_id_assign = tk.Label(
            self.tab_assign_asset, text="Employee ID:")
        self.label_employee_id_assign.grid(row=1, column=0)
        self.entry_employee_id_assign = tk.Entry(self.tab_assign_asset)
        self.entry_employee_id_assign.grid(row=1, column=1)

        self.button_assign_asset = tk.Button(
            self.tab_assign_asset, text="Assign Asset", command=self.assign_asset)
        self.button_assign_asset.grid(row=2, columnspan=2)

    def insert_employee(self):
        employee_id = self.entry_employee_id.get()
        name = self.entry_name.get()
        emp_location = self.entry_emp_location.get()
        phone_number = self.entry_phone_number.get()

        if check_employee_exists(employee_id):
            messagebox.showerror("insert employee error",
                                 f"employee with id {employee_id} already exists")
            return

        if len(phone_number) < 10:
            messagebox.showerror("Insert Employee Error",
                                 "Phone number must be at least 10 digits.")
            return

        insert_employee(employee_id, name, emp_location, phone_number)
        messagebox.showinfo("Insert Employee",
                            "Employee inserted successfully.")

    def insert_asset(self):
        asset_id = self.entry_asset_id.get()
        asset_name = self.entry_asset_name.get()
        asset_type = self.entry_asset_type.get()
        purchase_date = self.entry_purchase_date.get()
        location = self.entry_location.get()
        assigned_emp_id = self.entry_assigned_emp_id.get()
        notes = self.entry_notes.get()

        if self.entry_location.get() == "":
            print("location should not be empty")
            return

        if check_asset_exists(asset_id):
            messagebox.showerror("insert asset error",
                                 f"asset with id {asset_id} already exists")
            return
        insert_asset(asset_id, asset_name, asset_type, purchase_date, location,
                     assigned_emp_id, notes)
        messagebox.showinfo("Insert Asset", "Asset inserted successfully.")

    def update_asset(self):
        asset_id = self.entry_asset_id_update.get()
        new_asset_name = self.entry_new_asset_name.get()
        new_asset_type = self.entry_new_asset_type.get()
        new_purchase_date = self.entry_new_purchase_date.get()
        new_location = self.entry_new_location.get()
        new_assigned_emp_id = self.entry_new_assigned_emp_id.get()
        new_notes = self.entry_new_notes.get()

        update_asset(asset_id, new_asset_name, new_asset_type, new_purchase_date, new_location,
                     new_assigned_emp_id, new_notes)
        messagebox.showinfo("update Asset", "Asset updates successfully.")

    def delete_asset(self):
        asset_id = self.entry_asset_id.get()

        delete_asset(asset_id)
        messagebox.showinfo("Delete Asset", "Asset deleted successfully.")

    def view_asset(self):
        asset_id = self.entry_asset_id.get()
        asset_values = view_asset(asset_id)

        if asset_values:
            popup = Toplevel(self.root)
            popup.title("view asset")

            text = "Asset Id\tAsset Name\tAsset Type\tpurchase date\tlocation\tassigned_employe_id\tnotes\n"
            text += "--------------------------------------------------------------------------------------------\n"

            asset_id, asset_name, asset_type, purchase_date, location, assigned_emp_id, notes = asset_values
            text += f"{asset_id}\t{asset_name}\t{asset_type}\t{purchase_date}\t{location}\t{assigned_emp_id}\t{notes}\n"

            label_asset_values = tk.Label(popup, text=text, justify="left")
            label_asset_values.pack()
        else:
            messagebox.showinfo(
                "View Asset", f"No asset found with ID: {asset_id}")

    def assign_asset(self):
        asset_id = self.entry_asset_id_assign.get()
        employee_id = self.entry_employee_id_assign.get()

        assign_asset(asset_id, employee_id)
        messagebox.showinfo("Assign Asset", "Asset assigned successfully.")


# Initialize Tkinter
root = tk.Tk()
app = AssetManagementGUI(root)
root.mainloop()
