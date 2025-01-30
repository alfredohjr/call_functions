from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai.chat_models import ChatOpenAI

from src.tools.the_wikipedia import the_wikipedia
from src.tools.the_email_sender import send_email
from src.tools.the_best_clients import the_best_clients

MODEL = "qwen2.5-3b-instruct"
HOST = "http://127.0.0.1:1234/v1"

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


tools = [add, multiply, the_wikipedia, send_email, the_best_clients]

prompt_template = "{user_input} {agent_scratchpad}"
prompt = PromptTemplate(
    input_variables=["user_input","agent_scratchpad"], template=prompt_template
)
llm = ChatOpenAI(base_url=HOST, model=MODEL, api_key='lm-studio')

llm.bind_tools(tools)

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(agent_executor.invoke({'user_input':"Procure os melhores clientes, para cada cliente pesquise uma fruta aleatoria na wikipedia e mande um email para ele explicando a vantagem dela."}))