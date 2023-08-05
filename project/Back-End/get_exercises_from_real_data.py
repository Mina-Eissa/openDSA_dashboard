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


@router.get("/api/get_exercises")
def get_exercises():
    mycursor = mydb.cursor()
    query = "select distinct question_id,question_name from summeddata1\
            order by question_id; "
    mycursor.execute(query)
    result = mycursor.fetchall()
    data = {"Exercise":[]}
    for row in result:
        record = {}
        record["Exercise_ID"] = row[0]
        record["Exercise_name"] = row[1]
        data["Exercise"].append(record)
    
    json_data=jsonable_encoder(data)
    return json_data
