from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from girth import twopl_mml
import pandas as pd
import numpy as np

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Matrix(BaseModel):
    data: list[list[float]]


class InputData(BaseModel):
    matrix: Matrix
    ability: list[float] = []


@app.post("/estimate")
def estimate_item_params(data: InputData):
    matrix_data = pd.DataFrame(data.matrix.data)
    matrix_data = matrix_data.dropna().astype(int).values
    if data.ability:
        ability = data.ability
    else:
        ability = matrix_data.sum(axis=0)
    ability = np.interp(ability, (ability.min(), ability.max()), (-2, 2))
    estimates = twopl_mml(matrix_data)
    discrimination = estimates['Discrimination'].tolist()
    difficulty = estimates['Difficulty'].tolist()
    print(discrimination[0])
    print(difficulty[0])
    print(ability)
    return {
        'Discrimination': discrimination,
        'Difficulty': difficulty,
        'Ability': ability.tolist(),
    }
    


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)