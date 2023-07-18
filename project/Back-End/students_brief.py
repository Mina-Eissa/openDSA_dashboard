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


@router.post("/api/students_brief/")
def students_brief(BID=None):
    cursor = mydb.cursor()
    if BID == None:
        return jsonable_encoder({"error":"there's no book chosen"})
    else:
        cursor.execute("SELECT DISTINCT BOOKID FROM BOOK WHERE BOOKID =%s",(BID,))
        if len(cursor.fetchall())==0:
            return jsonable_encoder({"error":"this book is does not exist"})
        
    query ="SELECT SB.SID,CONCAT(S.SFIRST_NAME,' ',S.SLAST_NAME) AS NAME,\
            SB.NUMBER_OF_ATTEMPTS AS ATTEMPTS,SB.NUMBER_OF_INCORRECT_ATTEMPTS AS INCORRECT_ATTEMPTS\
            ,SB.NUMBER_OF_HINTS AS HINTS,SB.TIMESPENT AS TIMESPENT FROM STUDENT_BOOK AS SB\
            JOIN STUDENT AS S\
            ON S.SID=SB.SID\
            WHERE BID=%s;"
    cursor.execute(query,(BID,))
    results = cursor.fetchall()
    data =[]
    for row in results:
        record = {}
        record["Student_ID"]=row[0]
        record["Student_Name"]=row[1]
        record["Attempts"]=row[2]
        record["Incorrect_Attempts"]=row[3]
        record["Time_Spent"]=row[4]
        data.append(record)
    json_data=jsonable_encoder(data)
    return json_data
    
    
