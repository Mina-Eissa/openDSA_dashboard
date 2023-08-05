from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from girth import twopl_mml
import pandas as pd
import numpy as np

router = APIRouter()


class Matrix(BaseModel):
    data: list[list[float]]


class InputData(BaseModel):
    matrix: Matrix
    ability: list[float] = []


@router.post("/estimate2")
def estimate_item_params(data: InputData):
    matrix_data = pd.DataFrame(data.matrix.data)
    matrix_data = matrix_data.dropna().astype(int).values
    if data.ability:
        ability = data.ability
    else:
        ability = matrix_data.sum(axis=1)
    ability = np.interp(ability, (ability.min(), ability.max()), (-50, 50))
    estimates = twopl_mml(matrix_data)
    discrimination = estimates['Discrimination'].tolist()
    difficulty = estimates['Difficulty'].tolist()
    return {
        'Discrimination': discrimination,
        'Difficulty': difficulty,
        'Ability': ability.tolist(),
    }
