from fastapi import FastAPI
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

router = APIRouter()
def excute_query(query):
    mycursor = mydb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

@router.get("/api/get_books_data")
async def get_books_data():
    query="select bookid, bname from book"
    books = excute_query(query)
    query = "select chid, chname, bookid from chapter\
                order by bookid"
    chapters = excute_query(query)
    query = "select secid, secname, chid from section\
                order by chid"
    sections = excute_query(query)
    query = "select exid, exname , secid from exercise\
                order by secid"
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
                row_dict["id"]=row[0]
                row_dict["name"]=row[1]
                row_dict["exercises"] = arrange_exercises(row[0])
                data.append(row_dict)
        return data
    def arrange_chapters(bookid):
        data=[]
        for row in chapters:
            row_dict = {}
            if row[2] == bookid:
                row_dict["id"]=row[0]
                row_dict["name"]=row[1]
                row_dict["sections"] = arrange_sections(row[0])
                data.append(row_dict)
        return data
    def arrange_books():
        data = []
        for row in books:
            row_dict = {}
            row_dict["id"]=row[0]
            row_dict["name"]=row[1]
            row_dict["chapters"] = arrange_chapters(row[0])
            data.append(row_dict)
        return data
    
    json_data = jsonable_encoder(arrange_books())
    print(json_data)
    return json_data
