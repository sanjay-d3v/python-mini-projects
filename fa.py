import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Employee(BaseModel):
    employee_id: int
    name: str
    emp_location: str
    phone_number: str


class Asset(BaseModel):
    asset_id: int
    asset_name: str
    asset_type: str
    purchase_date: str
    location: str
    assigned_emp_id: int
    notes: str


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


@app.post("/employees/, tags = [add new employee]")
def create_employee(employee: Employee):
    insert_employee(**employee)
    return {"message": "Employee created"}


@app.post("/assets/")
def create_asset(asset: Asset):
    insert_asset(**asset.dict())
    return {"message": "Asset created"}


@app.put("/assets/assign/{asset_id}/{employee_id}")
def assign_asset_endpoint(asset_id: int, employee_id: int):
    if not check_employee_exists(employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    if not check_asset_exists(asset_id):
        raise HTTPException(status_code=404, detail="Asset not found")

    assign_asset(asset_id, employee_id)
    return {"message": "Asset assigned"}


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):
    asset = view_asset(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    employee = view_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):
    if not check_asset_exists(asset_id):
        raise HTTPException(status_code=404, detail="Asset not found")

    delete_asset(asset_id)
    return {"message": "Asset deleted"}
