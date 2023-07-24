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
        cursor.execute("select distinct id from inst_books where id=%s",(BID,))
        if len(cursor.fetchall())==0:
            return jsonable_encoder({"error":"this book is does not exist"})
    
    query_chapters = "select distinct ch.id as ChapterID ,ch.name as ChapterName from inst_chapters as ch where inst_book_id=%s"
    query_sections = "select distinct inst_modules.id as ModID,inst_modules.name as ModName\
                    from inst_modules\
                    join inst_chapter_modules\
                    on inst_chapter_modules.inst_module_id=inst_modules.id\
                    join inst_chapters\
                    on inst_chapters.id = inst_chapter_modules.inst_chapter_id\
                    where inst_chapters.inst_book_id = %s;"
    query_exercises = "select distinct inst_exercises.id as EXEID,inst_exercises.name as EXEName\
                    from inst_exercises\
                    join inst_module_section_exercises\
                    on inst_module_section_exercises.inst_exercise_id = inst_exercises.id\
                    join inst_module_versions\
                    on inst_module_versions.id = inst_module_section_exercises.inst_module_version_id\
                    join inst_modules \
                    on inst_modules.id = inst_module_versions.inst_module_id\
                    join inst_chapter_modules\
                    on inst_chapter_modules.inst_module_id=inst_modules.id\
                    join inst_chapters\
                    on inst_chapters.id = inst_chapter_modules.inst_chapter_id\
                    where inst_chapters.inst_book_id = %s;"
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
    
    query_sections = "select distinct inst_modules.id as ModID,inst_modules.name as ModName\
                    from inst_modules\
                    join inst_chapter_modules\
                    on inst_chapter_modules.inst_module_id=inst_modules.id\
                    join inst_chapters\
                    on inst_chapters.id = inst_chapter_modules.inst_chapter_id\
                    where inst_chapters.id in ({})".format(",".join(["%s"] * len(listOfChapters.Choices)))
    query_exercises = "select distinct inst_exercises.id as EXEID,inst_exercises.name as EXEName\
                    from inst_exercises\
                    join inst_module_section_exercises\
                    on inst_module_section_exercises.inst_exercise_id = inst_exercises.id\
                    join inst_module_versions\
                    on inst_module_versions.id = inst_module_section_exercises.inst_module_version_id\
                    join inst_modules \
                    on inst_modules.id = inst_module_versions.inst_module_id\
                    join inst_chapter_modules\
                    on inst_chapter_modules.inst_module_id=inst_modules.id\
                    join inst_chapters\
                    on inst_chapters.id = inst_chapter_modules.inst_chapter_id\
                    where inst_chapters.id in ({})".format(",".join(["%s"] * len(listOfChapters.Choices)))
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
    
    query_exercises = "select distinct inst_exercises.id as EXEID,inst_exercises.name as EXEName\
                    from inst_exercises\
                    join inst_module_section_exercises\
                    on inst_module_section_exercises.inst_exercise_id = inst_exercises.id\
                    join inst_module_versions\
                    on inst_module_versions.id = inst_module_section_exercises.inst_module_version_id\
                    join inst_modules \
                    on inst_modules.id = inst_module_versions.inst_module_id\
                    join inst_chapter_modules\
                    on inst_chapter_modules.inst_module_id=inst_modules.id\
                    where inst_modules.id in ({})".format(",".join(["%s"] * len(listOfSections.Choices)))
    data= {}
    data["Exercises"] = get_exercises(query_exercises,listOfSections.Choices)

    json_data=jsonable_encoder(data)
    return json_data