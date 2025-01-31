from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai.chat_models import ChatOpenAI

from src.tools.the_imdb import the_get_columns, the_get_total_by_column, the_get_vote_average_by_column, the_get_a_random_movie

MODEL = "qwen2.5-3b-instruct"
HOST = "http://127.0.0.1:1234/v1"


tools = [the_get_columns, the_get_total_by_column, the_get_vote_average_by_column, the_get_a_random_movie]

prompt_template = "{user_input} {agent_scratchpad}"
prompt = PromptTemplate(
    input_variables=["user_input","agent_scratchpad"], template=prompt_template
)
llm = ChatOpenAI(base_url=HOST, model=MODEL, api_key='lm-studio')

llm.bind_tools(tools)

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(agent_executor.invoke({'user_input':"me de a sugestao de algum filme, pegue as informacoes e faça um resumo atrativo", 'agent_scratchpad':""}))