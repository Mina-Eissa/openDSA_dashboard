from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from pydantic import BaseModel
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
cursor = mydb.cursor()

router = APIRouter()

class ListOfChoices(BaseModel):
    Choices : list[int]

@router.get('/api/Filtered_Student_bu_Exercises/')
def get_students(listOfExercises:ListOfChoices):
    if len(listOfExercises.Choices)==0:
        ret={"Student":[]}
        return jsonable_encoder(ret)
    
    query="SELECT S.SID AS ID ,CONCAT(S.SFIRST_NAME,' ',S.SLAST_NAME) AS NAME,\
            SUM(SE.NUMBER_OF_ATTEMPTS) AS ALL_ATTEMPTS,SUM(SE.NUMBER_OF_INCORRECT_ATTEMPTS) AS INCORRECT_ATTEMPTS,\
            SUM(SE.NUMBER_OF_HINTS) AS HINTS,SUM(SE.TIMESPENT)  AS TIME\
            FROM STUDENT AS S\
            JOIN STUDENT_EXERCISE AS SE\
            ON SE.SID = S.SID\
            WHERE SE.EXID IN ({})\
            GROUP BY S.SID\
            ORDER BY S.SID ASC".format(",".join(["%s"] * len(listOfExercises.Choices)))
    
    cursor.execute(query,listOfExercises.Choices)
    data = cursor.fetchall()

    result = []
    for row in data:
        record = {}
        record["Student_ID"] = row[0]
        record["Studnet_Name"] =row[1]
        record["All_Attempts"]= row[2]
        record["Incorrect_Attempts"]= row[3]
        record["Hints"] = row[4]
        record["Time"] = row[5]
        result.append(record)
    
    json_res= jsonable_encoder(result)
    return json_res