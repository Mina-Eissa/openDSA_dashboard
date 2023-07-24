from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
import mysql.connector

from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file
mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

router = APIRouter()


@router.get("/api/get_books")
def get_books():
    mycursor = mydb.cursor()
    query = "select id ,title from inst_books"
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
