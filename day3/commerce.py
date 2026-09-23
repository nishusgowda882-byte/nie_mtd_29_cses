```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from pymongo import MongoClient
from bson import ObjectId

# app
app = FastAPI()

# db config
URL = "mongodb://127.0.0.1:27017"
client = MongoClient(URL)
db = client["ecommerce_support_db"]
support_collection = db["support_tickets"]

# schema pydantic
class SupportTicketCreate(BaseModel):
    customer_name: str
    email: str
    subject: str
    description: str
    category: str
    status: str


class SupportTicketResponse(SupportTicketCreate):
    id: str


# helper
def support_ticket_helper(ticket_doc):
    return {
        "id": str(ticket_doc["_id"]),
        "customer_name": ticket_doc["customer_name"],
        "email": ticket_doc["email"],
        "subject": ticket_doc["subject"],
        "description": ticket_doc["description"],
        "category": ticket_doc["category"],
        "status": ticket_doc["status"]
    }


# APIs - CRUD
# create, read all, read by id, update, delete


# CREATE
@app.post(
    "/support-tickets",
    status_code=201,
    response_model=SupportTicketResponse
)
def support_ticket_create(payload: SupportTicketCreate):

    ticket_dict = payload.model_dump()

    result = support_collection.insert_one(ticket_dict)

    new_ticket = support_collection.find_one(
        {"_id": result.inserted_id}
    )

    return support_ticket_helper(new_ticket)


# READ ALL
@app.get(
    "/support-tickets",
    response_model=list[SupportTicketResponse]
)
def support_ticket_read_all():

    docs = support_collection.find()

    tickets = [
        support_ticket_helper(doc)
        for doc in docs
    ]

    return tickets


# READ BY ID
@app.get(
    "/support-tickets/{id}",
    response_model=SupportTicketResponse
)
def support_ticket_read_by_id(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid Support Ticket ID",
            status_code=400
        )

    doc = support_collection.find_one(
        {"_id": ObjectId(id)}
    )

    if not doc:
        raise HTTPException(
            detail="Support Ticket Not Found",
            status_code=404
        )

    return support_ticket_helper(doc)


# UPDATE
@app.put(
    "/support-tickets/{id}",
    response_model=SupportTicketResponse
)
def support_ticket_update(
    id: str,
    payload: SupportTicketCreate
):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid Support Ticket ID",
            status_code=400
        )

    ticket_dict = payload.model_dump()

    result = support_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": ticket_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(
            detail="Support Ticket Not Found",
            status_code=404
        )

    new_ticket = support_collection.find_one(
        {"_id": ObjectId(id)}
    )

    return support_ticket_helper(new_ticket)


# DELETE
@app.delete("/support-tickets/{id}")
def support_ticket_delete(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid Support Ticket ID",
            status_code=400
        )

    result = support_collection.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            detail="Support Ticket Not Found",
            status_code=404
        )

    return {
        "message": "Support Ticket Deleted Successfully"
    }
