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
def excute_query(query):
    mycursor = mydb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

@router.get("/api/get_books_data")
async def get_books_data():
    query="select id , title from inst_books"
    books = excute_query(query)
    query = "select distinct id, name, inst_book_id from inst_chapters\
            order by inst_book_id"
    chapters = excute_query(query)
    query = "select distinct m.id, m.name, chmod.inst_chapter_id from inst_modules as m\
            join inst_chapter_modules as chmod\
            on chmod.inst_module_id = m.id\
            order by chmod.inst_chapter_id"
    sections = excute_query(query)
    query = "select distinct e.id,e.name,m.inst_module_id\
            from inst_exercises as e\
            join inst_module_section_exercises as mse\
            on mse.inst_exercise_id = e.id\
            join inst_module_versions as m\
            on m.id = mse.inst_module_version_id\
            order by m.inst_module_id"
    exercises = excute_query(query)


    def arrange_exercises(sectionid):
        data=[]
        for row in exercises:
            row_dict = {}
            if row[2] == sectionid:
                row_dict["id"]=row[0]
                row_dict["name"]=row[1]
                data.append(row_dict)
        return data
    def arrange_sections(chapterid):
        data=[]
        for row in sections:
            row_dict={}
            if row[2] == chapterid:
                row_dict["Section_id"]=row[0]
                row_dict["name"]=row[1]
                row_dict["exercises"] = arrange_exercises(row[0])
                data.append(row_dict)
        return data
    def arrange_chapters(bookid):
        data=[]
        for row in chapters:
            row_dict = {}
            if row[2] == bookid:
                row_dict["Chapter_id"]=row[0]
                row_dict["name"]=row[1]
                row_dict["sections"] = arrange_sections(row[0])
                data.append(row_dict)
        return data
    def arrange_books():
        data = []
        for row in books:
            row_dict = {}
            row_dict["Book_id"]=row[0]
            row_dict["name"]=row[1]
            row_dict["chapters"] = arrange_chapters(row[0])
            data.append(row_dict)
        return data
    
    json_data = jsonable_encoder(arrange_books())
    return json_data
