
from langchain.tools import tool
from pydantic import BaseModel
import pandas as pd

class The_netflix_by_type_Output(BaseModel):
    type: str
    total: int

@tool
def the_netflix_by_type() -> list[The_netflix_by_type_Output]:
    """
    Return a list of the types of movies and series available on Netflix.
    """
    df = pd.read_csv("tmp/netflix_titles.csv")
    df = df.value_counts("type").reset_index()
    types = []

    for _, v in df.iterrows():
        types.append(The_netflix_by_type_Output(type=v["type"], total=v['count']))
    return types

class The_netflix_get_columns_Output(BaseModel):
    name : str

@tool
def the_netflix_get_columns() -> list[The_netflix_get_columns_Output]:
    """
    Return a list of the columns in the Netflix dataset, use in the next tool to get the total of each value in a column.
    """
    df = pd.read_csv("tmp/netflix_titles.csv")
    return [The_netflix_get_columns_Output(name=col) for col in df.columns]

class The_netflix_get_total_by_column_Output(BaseModel):
    column : str
    name : str
    total : int

@tool
def the_netflix_get_total_by_column(column: str, top : int = 5) -> list[The_netflix_get_total_by_column_Output]:
    """
    args:
        column: str - The column to get the total of each value in the column.
        top: int - The number of top values to return.
        
    Return a list of the total of each value in a column.
    """
    df = pd.read_csv("tmp/netflix_titles.csv")
    df = df.value_counts(column).reset_index()
    values = []

    for _, v in df.iterrows():
        values.append(The_netflix_get_total_by_column_Output(column=column, name=str(v[column]), total=v['count']))
    return values[:top]