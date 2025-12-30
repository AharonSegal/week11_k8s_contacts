"""
This file handles AND all CRUD operations:

create_contact(contact_data: dict) → returns new contact ID as string
get_all_contacts() → returns list of Contact objects
update_contact(id: str, contact_data: dict) → returns success boolean
delete_contact(id: str) → returns success boolean

Handles errors with appropriate HTTP status codes

preview of a contact in the db:
    {'_id': ObjectId('6953af2451d6e1be82767fd1'), 
    'first_name': 'Korey', 
    'last_name': 'Steward', 
    'phone_number': '077-7934083'}
"""
from typing import List
from app.data.db_use import db


# contact fields to dict
def to_dict(first_name,last_name,phone_number) -> dict:
    return {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
    }


# ------------------------
# CRUD Functions
# ------------------------
#examples ----------
def create_contact(first_name: str, last_name: str, phone_number: str) -> int:
    contact_dict = to_dict(first_name,last_name,phone_number)
    result = db.Contacts.insert_one(contact_dict)
    return str(result.inserted_id)

def get_all_contacts():
    contacts = db.Contacts.find()
    # contacts is a object <pymongo.synchronous.cursor.Cursor object>
    # convert this obj to list
    return list(contacts)



# def create_contact(first_name: str, last_name: str, phone_number: str) -> int:
#     conn = get_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO contacts (first_name, last_name, phone_number) "
#             "VALUES (%s, %s, %s)",
#             (first_name, last_name, phone_number),
#         )
#         conn.commit()
#         return cursor.lastrowid
#     finally:
#         cursor.close()
#         conn.close()

# def db_get_contact(contact_id: int) -> dict | None:
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True) 
#     try:
#         cursor.execute("SELECT id, first_name, last_name, phone_number FROM contacts WHERE id=%s", (contact_id,))
#         row = cursor.fetchone()
#         return row  
#     finally:
#         cursor.close()
#         conn.close()

# def get_all_contacts() -> List[Contact]:
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
#     try:
#         cursor.execute("SELECT id, first_name, last_name, phone_number FROM contacts")
#         rows = cursor.fetchall()
#         # Convert each row dict into a Contact object
#         return [
#             Contact(
#                 id=row["id"],
#                 first_name=row["first_name"],
#                 last_name=row["last_name"],
#                 phone_number=row["phone_number"],
#             )
#             for row in rows
#         ]
#     finally:
#         cursor.close()
#         conn.close()


# def update_contact(contact_id: int, first_name: str, last_name: str, phone_number: str) -> bool:
#     conn = get_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "UPDATE contacts SET first_name=%s, last_name=%s, phone_number=%s "
#             "WHERE id=%s",
#             (first_name, last_name, phone_number, contact_id),
#         )
#         conn.commit()
#         return cursor.rowcount > 0
#     finally:
#         cursor.close()
#         conn.close()

# def delete_contact(contact_id: int) -> bool:
#     conn = get_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
#         conn.commit()
#         return cursor.rowcount > 0
#     finally:
#         cursor.close()
#         conn.close()

