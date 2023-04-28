from fastapi import FastAPI,Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from girth import twopl_mml
import pandas as pd
import numpy as np
import csv
import os
print(os.getcwd())


class Attempt:
    def __init__(self, user_id=0, ex_id=0, count_attempts=0, count_correct=0):
        self.user_id = user_id
        self.ex_id = ex_id
        self.count_attempts = count_attempts
        self.count_correct = count_correct
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/estimate/{string_input}")
def estimate_item_params(string_input: str):
    fileName = string_input
    print(fileName)
    try:
        with open(fileName, "r") as file:
            csvreader = csv.reader(file)
            next(csvreader) # skip header row
            attempts = []
            for row in csvreader:
                a, b, c, d = map(int, row)
                attempt = Attempt(a, b, c, d)
                attempts.append(attempt)
    except IOError as e:
        print(f"Could not open file: {e}")
        return 1

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

    matrix = [[False] * len(ex_map) for _ in range(len(user_map))]
    for attempt in attempts:
        if attempt.count_correct != 0:
            if attempt.count_attempts / attempt.count_correct >= 0.75:
                matrix[attempt.user_id][attempt.ex_id] = True
    matrix_data = np.array(matrix)
    matrix_data = matrix_data.astype(int)
    ability = matrix_data.sum(axis=1)
    ability = np.interp(ability, (ability.min(), ability.max()), (-20, 20))
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


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
