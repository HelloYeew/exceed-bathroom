from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from dateutil import parser
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient('mongodb://localhost', 27017)

db = client["bathroom"]

collection = db["room"]


class Bathroom(BaseModel):
    room_number: int
    status: bool
    last_update: str
    total_time: int
    total_session: int


# Reset all the data in the database to the default
@app.post('/bathroom/reset')
async def reset_bathroom():
    current_time = str(datetime.now())
    # Reset all the data in the database to the default
    for i in range(1, 4):
        # Find that is that room exist in database
        result = collection.find_one({"room_number": i})
        if result is None:
            # If not, create a new one
            collection.insert_one({
                "room_number": i,
                "status": False,
                "last_update": current_time,
                "total_time": 0,
                "total_session": 0}
            )
        else:
            # Update all value to default value
            collection.update_one({"room_number": i}, {"$set": {
                "room_number": i,
                "status": False,
                "last_update": current_time,
                "total_time": 0,
                "total_session": 0}}
                                  )
    return {"message": "Reset all the data in the database to the default successfully"}


# Return all the rooms
@app.get("/bathroom/get/all")
async def get_all_bathroom():
    r = list(collection.find({}, {"_id": 0}))
    if len(r) == 0:
        return {"message": "No data"}
    else:
        return r


# Return a specific room
@app.get("/bathroom/get/{room_number}")
async def get_bathroom(room_number: int):
    r = collection.find_one({"room_number": room_number}, {"_id": 0})
    if r is None:
        return {"message": "No data for this bathroom"}
    else:
        return r


# Return an average time for a specific room
@app.get("/bathroom/get/average/{room_number}/")
async def get_bathroom_average_time(room_number: int):
    r = collection.find_one({"room_number": room_number}, {"_id": 0})
    return {
        "total_time": r["total_time"],
        "total_session": r["total_session"],
        "average_time": r["total_time"] / r["total_session"]
    }


# Return an average time for all the rooms
@app.get("/bathroom/get/average/all")
async def get_all_bathroom_average_time():
    total_time_all_room = 0
    total_session_all_room = 0
    r = list(collection.find({}, {"_id": 0}))
    for i in r:
        total_time_all_room += i["total_time"]
        total_session_all_room += i["total_session"]
    if total_session_all_room == 0:
        return {
            "total_time_all_room": total_time_all_room,
            "total_session_all_room": total_session_all_room,
            "average_time": 0
        }
    return {
        "total_time_all_room": total_time_all_room,
        "total_session_all_room": total_session_all_room,
        "average_time": total_time_all_room / total_session_all_room
    }


# Put a new value to the target bathroom
@app.post("/bathroom/change/{room_number}/{status}")
async def change_bathroom_status(room_number: int, status: bool):
    r = collection.find_one({"room_number": room_number}, {"_id": 0})
    if r is None:
        return HTTPException(status_code=404, detail="Room not found")
    else:
        # Check if the status is not same with database for safety
        if r["status"] != status:
            # It can update the status
            # First case, just get in
            if r["status"] is False and status is True:
                # Update the status and last update time
                new_status = {
                    "status": status,
                    "last_update": str(datetime.now())
                }
                collection.update_one({"room_number": room_number}, {"$set": new_status})
            else:
                # Second case, just get out
                # Update the status, total
                # Calculate the total time in second
                total_time = r["total_time"] + (datetime.now() - parser.parse(r["last_update"])).total_seconds()
                new_status = {
                    "status": status,  # Update the status
                    "total_time": total_time,  # Update the total time
                    "last_update": str(datetime.now()),  # Update the last update time
                    "total_session": r["total_session"] + 1  # Update the total session
                }
                # Update the total time
                collection.update_one({"room_number": room_number}, {"$set": new_status})
        else:
            raise HTTPException(status_code=400, detail="Status is same with database")
    return {"message": "Update status success"}
