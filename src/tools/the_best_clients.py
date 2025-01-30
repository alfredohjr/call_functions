from langchain.tools import tool

@tool
def the_best_clients():
    """
    Returns a list of the best clients.
    """

    clients = ', '.join([f'Name: Client {i} and Email: client_{i}@localhost.com' for i in range(1, 5)])

    return f"The best clients are: {clients}"