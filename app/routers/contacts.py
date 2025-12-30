from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.data.data_interactor import (
    create_contact as db_create_contact,
    get_all_contacts as db_get_all_contacts,
    # update_contact as db_update_contact,
    # delete_contact as db_delete_contact,
    # db_get_contact as get_contact,
)

router = APIRouter(prefix="/contacts", tags=["Contacts"])


# ------------------------
# Pydantic Models / Schemas
# ------------------------
class ContactSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone_number: str = Field(min_length=1, max_length=20)


class ContactResponse(ContactSchema):
    id: str

class ContactUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

# ------------------------
# Helpers
# ------------------------
"""
makes the response dict
dict of contact including id
"""
def contact_helper(contact: dict) -> dict:
    return {
        "id": str(contact["_id"]),
        "first_name": contact["first_name"],
        "last_name": contact["last_name"],
        "phone_number": contact["phone_number"],
    }

# ------------------------
# API Endpoints
# ------------------------
"""
- Gets contact from user
- Adds it to the db
- Return the generated id
"""
@router.post("/")
def create_contact(contact: ContactSchema):
    try:
        # send to the db 
        new_id = db_create_contact(
            contact.first_name,
            contact.last_name,
            contact.phone_number,
        )
        return {"message": "Contact created successfully", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
- Returns Contact collection list
"""
@router.get("/", response_model=list[ContactResponse])
def list_contacts():
    try:
        contacts = db_get_all_contacts()
        return [contact_helper(c) for c in contacts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.put("/{contact_id}")
# def update_contact(contact_id: int, contact: ContactUpdateSchema):
#     try:
#         # input to dict
#         # exclude_unset=True -> tells Pydantic, only include fields that were sent by the client
#         # if the client did not enter `first_name`-> it is unset -> it will not be in the request
#         updates = contact.dict(exclude_unset=True)
#         # load contact 
#         existing = get_contact(contact_id)
#         # use new value if provided, otherwise old value
#         first_name  = updates.get("first_name",  existing["first_name"])
#         last_name   = updates.get("last_name",   existing["last_name"])
#         phone_value = updates.get("phone_number", existing["phone_number"])

#         # send to the db 
#         update_and_result = db_update_contact(contact_id, first_name, last_name, phone_value)

#         # success: return bool returned 
#         return {"success": update_and_result}
#     except Exception as e:
#         HTTPException(status_code=500, detail=str(e))


# @router.delete("/{contact_id}")
# def delete_contact(contact_id: int):
#     try:
#         # send to the db 
#         delete_and_result = db_delete_contact(contact_id)
#         # success: return bool returned 
#         return {"success": delete_and_result}
#     except Exception as e:
#         HTTPException(status_code=500, detail=str(e))