from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="dashboard"
)

router = APIRouter()


@router.get("/api/get_books")
def get_books():
    mycursor = mydb.cursor()
    query = "SELECT BookID, BNAME FROM BOOK "
    mycursor.execute(query)
    result = mycursor.fetchall()
    data = []
    for row in result:
        record = {}
        record["Book_ID"] = row[0]
        record["Book_name"] = row[1]
        data.append(record)
    
    json_data=jsonable_encoder(data)
    return json_data
