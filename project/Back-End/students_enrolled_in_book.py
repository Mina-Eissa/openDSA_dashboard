from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
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


@router.post("/api/students_enrolled_in_book/")
async def get_students_enrolled_in_book(BID: str):
    mycursor = mydb.cursor()

    mycursor.execute(
        "SELECT SID,CONCAT(SFIRST_NAME,' ',SLAST_NAME) as Name FROM student where SID in (Select SID from student_book where BID= %s)", (BID,))

    myresult = mycursor.fetchall()

    columns = [i[0] for i in mycursor.description]
    print(columns)
    # create a list of dictionaries representing the rows
    data = []
    for row in myresult:
        row_dict = {}
        for i in range(len(columns)):
            row_dict[columns[i]] = row[i]
        data.append(row_dict)

    json_data = jsonable_encoder(data)
    return json_data
