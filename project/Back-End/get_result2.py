from fastapi import FastAPI, Body
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from girth import twopl_mml
import pandas as pd
import numpy as np
import csv
import os
from pydantic import BaseModel
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)
cursor = mydb.cursor()
print(os.getcwd())


class Attempt:
    def __init__(self, ex_id="", user_id=0, count_attempts=0, count_correct=0):
        self.user_id = user_id
        self.ex_id = ex_id
        self.count_attempts = count_attempts
        self.count_correct = count_correct
    
    def __str__(self):
        return f"{self.user_id} {self.ex_id} {self.count_attempts} {self.count_correct}"


router = APIRouter()

def get_data():
    query = "select question_id,user_id,sum(count_attempts),sum(correct) from SummedData1\
            group by question_id,user_id \
            order by question_id"
    cursor.execute(query)
    data = cursor.fetchall()
    attempts = []
    for row in data:
        a, b, c, d = map(int,row)
        attempt = Attempt(a, b, c, d)
        attempts.append(attempt)
    return attempts
    
@router.get("/estimate/")
async def estimate_item_params():
    # fileName = string_input
    # print(fileName)
    # try:
    #     with open(fileName, "r") as file:
    #         csvreader = csv.reader(file)
    #         next(csvreader)  # skip header row
    #         attempts = []
    #         for row in csvreader:
    #             a, b, c, d = map(int, row)
    #             attempt = Attempt(a, b, c, d)
    #             attempts.append(attempt)
    # except IOError as e:
    #     print(f"Could not open file: {e}")
    #     return 1
    attempts = get_data()
    
    # for it in attempts:
    #     print(it)

    user_map = {}
    ex_map = {}
    for attempt in attempts:
        user_map[attempt.user_id] = None
        ex_map[attempt.ex_id] = None

    user_id = 0
    for user in user_map:
        user_map[user] = user_id
        user_id += 1

    ex_id = 0
    for ex in ex_map:
        ex_map[ex] = ex_id
        ex_id += 1

    for attempt in attempts:
        attempt.user_id = user_map[attempt.user_id]
        attempt.ex_id = ex_map[attempt.ex_id]

    matrix = [[False] * len(user_map) for _ in range(len(ex_map))]
    for attempt in attempts:
        if attempt.count_attempts != 0:
            if attempt.count_correct / attempt.count_attempts >= 0.75:
                matrix[attempt.ex_id][attempt.user_id] = True
    matrix_data = np.array(matrix)
    matrix_data = matrix_data.astype(int)
    ability = matrix_data.sum(axis=1)
    ability = np.interp(ability, (ability.min(), ability.max()), (-2, 2))
    estimates = twopl_mml(matrix_data)
    discrimination = estimates['Discrimination'].tolist()
    difficulty = estimates['Difficulty'].tolist()
    print(discrimination)
    print(difficulty)
    print(ability)

    return {
        'Discrimination': discrimination,
        'Difficulty': difficulty,
        'Ability': ability.tolist(),
    }
