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

@router.post('/api/Filtered_Student_by_Exercises/')
def get_students(listOfExercises:ListOfChoices):
    if len(listOfExercises.Choices)==0:
        ret={"Student":[]}
        return jsonable_encoder(ret)
    
    query="select distinct U.id as ID, concat(U.first_name,' ',U.last_name) as Name,sum(OXA.count_attempts),sum(OXP.total_correct),sum(OXA.count_hints),sum(OXA.time_taken)\
        from users as U\
        join odsa_exercise_attempts as OXA\
        on OXA.user_id = U.id\
        join inst_book_section_exercises as IBSE\
        on IBSE.id = OXA.inst_book_section_exercise_id\
        join odsa_exercise_progresses as OXP\
        on OXP.user_id = U.id\
        where IBSE.inst_exercise_id in ({})\
        group by U.id\
        order by U.id ASC".format(",".join(["%s"] * len(listOfExercises.Choices)))
    
    cursor.execute(query,listOfExercises.Choices)
    data = cursor.fetchall()

    result = []
    for row in data:
        record = {}
        record["Student_ID"] = row[0]
        record["Studnet_Name"] =row[1]
        record["All_Attempts"]= row[2]
        record["correct_Attempts"]= row[3]
        record["Hints"] = row[4]
        record["Time"] = row[5]
        result.append(record)
    
    json_res= jsonable_encoder(result)
    return json_res