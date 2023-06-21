from typing import List
from fastapi import FastAPI, Query
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
mycursor = mydb.cursor()

router = APIRouter()

@router.get('/api/Filtered_IRT/Chapters/')
def get_exercises(listOfChapters: str):

    chapter_ids =[]
    if listOfChapters.__contains__(","):
        chapter_ids = [int(chapter_id) for chapter_id in listOfChapters.split(',')]
    else:
        chapter_ids = [int(listOfChapters)]

    query = "SELECT EXID, SID, NUMBER_OF_ATTEMPTS AS ATTEMPTS, GREATEST(NUMBER_OF_ATTEMPTS - NUMBER_OF_INCORRECT_ATTEMPTS, 0) AS CORRECT FROM STUDENT_EXERCISE \
          WHERE CHID IN ({})".format(",".join(["%s"] * len(chapter_ids)))
    mycursor.execute(query, chapter_ids)
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
def get_exercises(listOfSections: str):
    section_ids = []
    if listOfSections.__contains__(","):
        section_ids = [int(section_id) for section_id in listOfSections.split(',')]
    else:
        section_ids = [int(listOfSections)]

    query = "SELECT EXID, SID, NUMBER_OF_ATTEMPTS AS ATTEMPTS, GREATEST(NUMBER_OF_ATTEMPTS - NUMBER_OF_INCORRECT_ATTEMPTS, 0) AS CORRECT FROM STUDENT_EXERCISE \
          WHERE SECID IN ({})".format(",".join(["%s"] * len(section_ids)))
    mycursor.execute(query, section_ids)
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
