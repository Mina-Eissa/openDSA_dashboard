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


@router.get("/api/student_book_data")
async def get_student_book_data():
    mycursor = mydb.cursor()
    mycursor.execute("WITH VIEW AS ( SELECT SE.SID ,SE.BOOKID ,S.SFIRST_NAME ,S.SLAST_NAME ,B.BNAME ,SE.NUMBER_OF_ATTEMPTS, SE.NUMBER_OF_HINTS ,SE.NUMBER_OF_INCORRECT_ATTEMPTS FROM STUDENT_EXERCISE AS SE JOIN STUDENT AS S ON SE.SID=S.SID JOIN BOOK AS B ON SE.BOOKID = B.BOOKID) SELECT CONCAT(SFIRST_NAME,' ',SLAST_NAME)AS STUDENT ,BNAME AS BOOK , SUM(NUMBER_OF_ATTEMPTS) AS EXERCISE_ATTEMPTS , SUM(NUMBER_OF_HINTS) AS HINTS_USED, SUM(NUMBER_OF_INCORRECT_ATTEMPTS) AS INCORRECT_ATTEMPTS FROM VIEW GROUP BY SID,BOOKID")
    myresult = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    # create a list of dictionaries representing the rows
    data = []
    for row in myresult:
        row_dict = {}
        for i in range(len(columns)):
            row_dict[columns[i]] = row[i]
        data.append(row_dict)
    json_data = jsonable_encoder(data)
    return json_data
