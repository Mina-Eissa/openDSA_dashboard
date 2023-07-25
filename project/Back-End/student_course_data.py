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


@router.post("/api/student_course_data")
async def get_student_course_data(CourseID):
    mycursor = mydb.cursor()
    query = "with students as(\
                select student.id as ID, concat(student.first_name,' ',student.last_name) as Name,\
                OXA.count_attempts as Attempts,OXA.correct as Correct , OXA.count_hints as Hints\
                from users as student\
                join odsa_exercise_attempts as OXA\
                on OXA.user_id = student.id\
                join course_enrollments as CE\
                on CE.user_id = student.id\
                join course_offerings as CF\
                on CF.id = CE.course_offering_id\
                join courses\
                on courses.id = CF.course_id\
                where courses.id = %s\
                )\
                select ID,Name,sum(Attempts) as Attempts,sum(Correct) as Correct,sum(Hints) as Hints\
                from students\
                group by ID\
                order by ID;"
    mycursor.execute(query,(CourseID,))
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
