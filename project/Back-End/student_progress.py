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
mycursor = mydb.cursor()


router = APIRouter()


def get_data(myresult, mycursor):
    cols = [i[0] for i in mycursor.description]
    row_dict = {}
    for i in range(len(cols)):
        if myresult[0][i] is not None:
            row_dict[cols[i]] = myresult[0][i]
        else:
            row_dict[cols[i]] = 0
    return row_dict


@router.get("/api/student_progress/")
async def get_students_enrolled_in_book(SID=None, BID=None, CHID=None, SECID=None):
    data = []
    if SID is None and BID is None and CHID is None and SECID is None:
        return data

    query_general = "SELECT SID,BID,SUM(NUMBER_OF_ATTEMPTS) AS BOOK_NUM_OF_ATTEMPTS,SUM(NUMBER_OF_HINTS) AS BOOK_NUM_OF_HINTS,SUM(NUMBER_OF_INCORRECT_ATTEMPTS) AS BOOK_NUM_OF_INCORRECT_ATTEMPTS,TIMESPENT FROM STUDENT_BOOK WHERE SID=%s AND BID=%s"
    query_chapter = "SELECT SID,CHID,SUM(NUMBER_OF_ATTEMPTS) AS CHAPTER_NUM_OF_ATTEMPTS,SUM(NUMBER_OF_HINTS) AS CHAPTER_NUM_OF_HINTS,SUM(NUMBER_OF_INCORRECT_ATTEMPTS) AS CHAPTER_NUM_OF_INCORRECT_ATTEMPTS,TIMESPENT FROM STUDENT_CHAPTER WHERE SID=%s AND CHID=%s"
    query_section = "SELECT SID,SECID,SUM(NUMBER_OF_ATTEMPTS) AS SECTION_NUM_OF_ATTEMPTS,SUM(NUMBER_OF_HINTS) AS SECTION_NUM_OF_HINTS,SUM(NUMBER_OF_INCORRECT_ATTEMPTS) AS SECTION_NUM_OF_INCORRECT_ATTEMPTS,TIMESPENT FROM STUDENT_SECTION WHERE SID=%s AND SECID=%s"

    mycursor.execute("Select concat(sfirst_name,' ',slast_name) as name from student\
                    where SID = %s ", (SID,))
    student_name = mycursor.fetchall()[0][0]
    
    mycursor.execute(query_general, (SID, BID,))
    myresult = mycursor.fetchall()
    if myresult is not None:
        row = get_data(myresult, mycursor)
        row["SID"] = int(SID)
        row["BID"] = int(BID)
        row["Name"] = student_name
        data.append(row)

    if CHID:
        mycursor.execute(query_chapter, (SID, CHID,))
        myresult = mycursor.fetchall()
        if myresult is not None:
            row = get_data(myresult, mycursor)
            row["SID"] = int(SID)
            row["CHID"] = int(CHID)
            row["Name"] = student_name
            data.append(row)

    if SECID:
        mycursor.execute(query_section, (SID, SECID,))
        myresult = mycursor.fetchall()
        if myresult is not None:
            row = get_data(myresult, mycursor)
            row["SID"] = int(SID)
            row["SECID"] = int(SECID)
            row["Name"] = student_name
            data.append(row)
    
    json_data = jsonable_encoder(data)
    return json_data
