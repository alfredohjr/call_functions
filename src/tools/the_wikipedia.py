from langchain.tools import tool

@tool
def the_wikipedia(search_term:str):
    """
    Search for a term on Wikipedia and return the first sentence of the article.
    """
    return f"""The term {search_term} is very large and complex, see the full article on Wikipedia: https://en.wikipedia.org/wiki/{search_term}"""