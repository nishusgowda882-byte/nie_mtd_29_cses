from fastapi import FastApi,HTTPExcepation
from pydantic import BaseModel
from pymongo import MongoClient
from bson import objectID
#app
app=FastApI()
#db config
URL="mongo://127.0.0.1.27017"
client=Mongoclient(URL)
db=client["service_ticket_db"]
ticket_collection=db["tickets"]
#schema pydantic
class TicketCreate(BaseModel):
    title:str
    descripation:str
    category:str
    status:str
class TicketResponse(TicketCreate):
    id:str
#helper
def ticket_helper(ticket_doc):
    return{
        "id":str(ticket_doc["_id"]),
        "title":ticket_doc["title"],
        "descripation":ticket_doc["descripation"],
        "category":ticket_doc["category"],
        "status":ticket_doc["status"]
    }
#api - CRUD - create,read all,read by id,update,delete
@app.post("/tickets",status_code=201,response_model=TicketResponse)
def ticket_create(payload:TicketCreate):
    ticket_dict=payload.model_dump()
    result=ticket_collection.insert_one(ticket_dict)
    new_ticket=ticket_helper(new_ticket)
    return ticket_helper(new_ticket)
@app.get("/tickets",response_model=list[TicketResponse])
def ticket_read_all():
    docs=ticket_collection.find()
    tickets=[ticket_helper(doc) for doc in docs]
    return tickets 
