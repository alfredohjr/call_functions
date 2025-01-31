from langchain.tools import tool
from pydantic import BaseModel

class The_Best_Clients_Output(BaseModel):
    name : str
    email : str

@tool
def the_best_clients() -> list[The_Best_Clients_Output]:
    """
    Returns a list of the best clients.
    """

    clients = []
    for i in range(1, 5):
        clients.append(
            The_Best_Clients_Output(
                name=f'Client {i}',
                email=f'client_{i}@gmail.com')
        )

    return clients