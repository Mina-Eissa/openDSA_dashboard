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

def get_chapters(query,params):
    cursor.execute(query,params)
    data = cursor.fetchall()
    result = []
    for row in data:
        record = {}
        record["Chapter_ID"] = row[0]
        record["Chapter_Name"] = row[1]
        result.append(record)
    return result


def get_sections(query,params):
    cursor.execute(query,params)
    data = cursor.fetchall()
    result = []
    for row in data:
        record = {}
        record["Section_ID"] = row[0]
        record["Section_Name"] = row[1]
        result.append(record)
    return result

def get_exercises(query,params):
    cursor.execute(query,params)
    data = cursor.fetchall()
    result = []
    for row in data:
        record = {}
        record["Exercise_ID"] = row[0]
        record["Exercise_Name"] = row[1]
        result.append(record)
    return result

@router.post('/api/Filtered_Book/Book/')
def get_chapters_and_sections_and_exercises_(BID=None):
    message = ""
    if BID is None:
        message ="There's no BOOKID chosen!!"
        return jsonable_encoder({"error":message})
    else:
        cursor.execute("SELECT DISTINCT BOOKID FROM BOOK WHERE BOOKID =%s",(BID,))
        if len(cursor.fetchall())==0:
            return jsonable_encoder({"error":"this book is does not exist"})
    
    query_chapters = "SELECT DISTINCT CHID,CHNAME FROM CHAPTER WHERE BOOKID =%s "
    query_sections = "SELECT SECID ,SECNAME FROM SECTION AS SEC\
                        JOIN CHAPTER AS CH ON CH.CHID = SEC.CHID\
                        WHERE BOOKID =%s"
    query_exercises = "SELECT DISTINCT EX.EXID ,EX.EXNAME FROM EXERCISE AS EX\
                        JOIN STUDENT_EXERCISE  AS SE ON EX.EXID = SE.EXID\
                        WHERE BOOKID = %s"
    data= {}
    data["Chapters"] = get_chapters(query_chapters,(BID,))
    data["Sections"] = get_sections(query_sections,(BID,))
    data["Exercises"] = get_exercises(query_exercises,(BID,))

    json_data = jsonable_encoder(data)
    return json_data



@router.post('/api/Filtered_Book/Chapter/')
def get_sections_and_exercises_(listOfChapters:ListOfChoices):
    if len(listOfChapters.Choices)==0:
        ret = {"Sections":[],"Exercises":[]}
        return jsonable_encoder(ret)
    
    query_sections = "SELECT SECID ,SECNAME FROM SECTION\
                        WHERE CHID in ({})".format(",".join(["%s"] * len(listOfChapters.Choices)))
    query_exercises = "SELECT DISTINCT EX.EXID ,EX.EXNAME FROM EXERCISE AS EX\
                        JOIN STUDENT_EXERCISE  AS SE ON EX.EXID = SE.EXID\
                        WHERE CHID in ({})".format(",".join(["%s"] * len(listOfChapters.Choices)))
    data= {}
    data["Sections"] = get_sections(query_sections,listOfChapters.Choices)
    data["Exercises"] = get_exercises(query_exercises,listOfChapters.Choices)

    json_data=jsonable_encoder(data)
    return json_data

@router.post('/api/Filtered_Book/Section/')
def get_exercises_(listOfSections:ListOfChoices):
    if len(listOfSections.Choices)==0:
        ret = {"Exercises":[]}
        return jsonable_encoder(ret)
    
    query_exercises = "SELECT DISTINCT EX.EXID ,EX.EXNAME FROM EXERCISE AS EX\
                        JOIN STUDENT_EXERCISE  AS SE ON EX.EXID = SE.EXID\
                        WHERE SE.SECID in ({})".format(",".join(["%s"] * len(listOfSections.Choices)))
    data= {}
    data["Exercises"] = get_exercises(query_exercises,listOfSections.Choices)

    json_data=jsonable_encoder(data)
    return json_data