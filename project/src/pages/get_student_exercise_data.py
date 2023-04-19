from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="A2s91!!??",
  database="dashboard"
)

mycursor = mydb.cursor()

mycursor.execute("WITH VIEW AS ( SELECT SE.SID ,SE.BOOKID ,S.SFIRST_NAME ,S.SLAST_NAME ,B.BNAME ,SE.NUMBER_OF_ATTEMPTS, SE.NUMBER_OF_HINTS ,SE.NUMBER_OF_INCORRECT_ATTEMPTS FROM STUDENT_EXERCISE AS SE JOIN STUDENT AS S ON SE.SID=S.SID JOIN BOOK AS B ON SE.BOOKID = B.BOOKID) SELECT CONCAT(SFIRST_NAME,' ',SLAST_NAME)AS STUDENT ,BNAME AS BOOK , COUNT(NUMBER_OF_ATTEMPTS) AS EXERCISE_ATTEMPTS , SUM(NUMBER_OF_HINTS) AS HINTS_USED, SUM(NUMBER_OF_INCORRECT_ATTEMPTS) AS INCORRECT_ATTEMPTS FROM VIEW GROUP BY SID,BOOKID")

myresult = mycursor.fetchall()

columns = [i[0] for i in mycursor.description]

# create a list of dictionaries representing the rows
data = []
for row in myresult:
    row_dict = {}
    for i in range(len(columns)):
        row_dict[columns[i]] = row[i]
    data.append(row_dict)


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/student_exercise_data")
async def get_student_exercise_data():
    json_data = jsonable_encoder(data)
    return json_data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)



