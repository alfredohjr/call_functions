from langchain.tools import tool
from pydantic import BaseModel
import pandas as pd

FILE = "tmp/tmdb_5000_movies.csv"
df = pd.read_csv(FILE)
df = df.sample(1000)

def extract_to_vector_db():
    df = pd.read_csv(FILE)
    f = open("tmp/imdb_titles_overview.txt", "w", encoding='utf-8')
    for _, v in df.iterrows():
        title = v['title']
        overview = v['overview']
        f.write(f"{title} | {overview}\n")
    f.close()


class The_get_columns_Output(BaseModel):
    name : str

@tool
def the_get_columns() -> list[The_get_columns_Output]:
    """
    Return a list of the columns of the dataset, if very important to choice the right column to work with.
    """
    return [The_get_columns_Output(name=col) for col in df.columns]


class The_get_total_by_column_Output(BaseModel):
    column : str
    name : str
    total : int

@tool
def the_get_total_by_column(column: str, top : int = 5) -> list[The_get_total_by_column_Output]:
    """
    args:
        column: str - The column to get the total of each value in the column.
        top: int - The number of top values to return.
        
    Return a list of the total of each value in a column.
    """

    tmp = df.value_counts(column).reset_index()
    values = []

    for _, v in tmp.iterrows():
        values.append(The_get_total_by_column_Output(column=column, name=str(v[column]), total=v['count']))
    return values[:top]


class The_get_vote_average_by_column_Output(BaseModel):
    column : str
    name : str
    vote_average : float

@tool
def the_get_vote_average_by_column(column: str, top: int = 5) -> list[The_get_vote_average_by_column_Output]:
    """
    This function calculates the vote average of each value in a column.

    args:
        column: str - The column to get the vote average of each value in the column.
        top: int - The number of top values to return.
        
    Return a list of the vote average of each value in a column.
    """

    tmp = df.groupby(column)["vote_average"].mean().reset_index()
    values = []
    for _, v in tmp.iterrows():
        values.append(The_get_vote_average_by_column_Output(column=column, name=v[column], vote_average=v["vote_average"]))
    return values


@tool
def the_get_a_random_movie() -> str:
    """
    Return a random movie from the dataset.
    """
    return f"{df.sample(1).to_string(index=False)}"


if __name__ == '__main__':
    extract_to_vector_db()