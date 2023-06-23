from typing import List
from fastapi import Body, FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
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
mycursor = mydb.cursor()

router = APIRouter()

class ListOfChoices(BaseModel):
    Choices : list[int]



@router.get('/api/Filtered_IRT/Chapters/')
def get_exercises(listOfChapters: ListOfChoices):

    print(listOfChapters.Choices)
    query = "SELECT DISTINCT EXID, SID, NUMBER_OF_ATTEMPTS AS ATTEMPTS, GREATEST(NUMBER_OF_ATTEMPTS - NUMBER_OF_INCORRECT_ATTEMPTS, 0) AS CORRECT FROM STUDENT_EXERCISE \
          WHERE CHID IN ({})".format(",".join(["%s"] * len(listOfChapters.Choices)))
    mycursor.execute(query, listOfChapters.Choices)
    data = mycursor.fetchall()
    listOfExe = []
    for row in data:
        record = {}
        record["exercise_id"] = row[0]
        record["student_id"] = row[1]
        record["attempts"] = row[2]
        record["correct"] = row[3]
        listOfExe.append(record)
    json_result = jsonable_encoder(listOfExe)
    return json_result


@router.get('/api/Filtered_IRT/Sections/')
def get_exercises(listOfSections: ListOfChoices):
    
    query = "SELECT DISTINCT EXID, SID, NUMBER_OF_ATTEMPTS AS ATTEMPTS, GREATEST(NUMBER_OF_ATTEMPTS - NUMBER_OF_INCORRECT_ATTEMPTS, 0) AS CORRECT FROM STUDENT_EXERCISE \
          WHERE SECID IN ({})".format(",".join(["%s"] * len(listOfSections.Choices)))
    
    mycursor.execute(query, listOfSections.Choices)
    data = mycursor.fetchall()
    listOfExe = []
    for row in data:
        record = {}
        record["exercise_id"] = row[0]
        record["student_id"] = row[1]
        record["attempts"] = row[2]
        record["correct"] = row[3]
        listOfExe.append(record)
    json_result = jsonable_encoder(listOfExe)
    return json_result
