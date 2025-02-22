import os
from pathlib import Path

from dotenv import load_dotenv
from phi.agent import Agent, AgentMemory, RunResponse
from phi.memory.classifier import MemoryClassifier
from phi.memory.db.sqlite import SqliteMemoryDb
from phi.memory.summarizer import MemorySummarizer
from phi.model.aws.claude import Claude
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.tools.file import FileTools
from phi.tools.tavily import TavilyTools
from phi.tools.yfinance import YFinanceTools
from phi.agent.python import PythonAgent
from phi.utils.log import logger

from src.plugins import WarehousePlugin, FilePlugin

load_dotenv()

tavily_tools = TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))
warehouse_plugin = WarehousePlugin(format_type="markdown")
file_plugin = FilePlugin()

bedrock_model = Claude(id="anthropic.claude-3-5-sonnet-20240620-v1:0")

### Persist Memories ###
leader_memory = SqliteMemoryDb(db_file="db/leader_memory.db")
warehouse_memory = SqliteMemoryDb(db_file="db/warehouse_memory.db")
search_memory = SqliteMemoryDb(db_file="db/search_memory.db")
file_memory = SqliteMemoryDb(db_file="db/file_memory.db")
leader_storage = SqlAgentStorage(
    table_name="agent_sessions", db_file="db/agent_storage.db"
)


def generate_memory_db(db_file: str) -> AgentMemory:
    return AgentMemory(
        db=SqliteMemoryDb(db_file=db_file)
    )


cwd = Path(__file__).parent.resolve()
tmp = cwd.joinpath("tmp")
if not tmp.exists():
    tmp.mkdir(exist_ok=True, parents=True)

python_agent = PythonAgent(
    name="PythonAgent",
    model=bedrock_model,
    base_dir=tmp,
    role="Python Developer",
    description="""
    You are a python developer that can write code in python.
    """,
    instructions="""
    ** Instructions **
    - You are full authority to write code in python.
    - Generate chart or calcualtions in python to help the manager to make decisions.
    - You can use the FilePlugin to read and write files.
    - Generate charts as png files.
    - Generate csv files to help the manager to make decisions.
    """,
    tools= [file_plugin],
    markdown=True,
    pip_install=True,
    show_tool_calls=True,
    structured_output=True,
)

researcher_agent = Agent(
    name="ResearcherAgent",
    model=bedrock_model,
    role="Researcher",
    description="""
    You are a researcher that can check trending products to sale or financial statues of our rivals.
    You can also check the customers and their preferences.
    """,
    instructions="""
    ** Instructions **
    - You are a researcher that can check trending products to sale or financial statues of our rivals.
    - You can also check the customers and their preferences.
    - You can use the TavilyTools to search the web for information and Crawl4aiTools to crawl the web for information.
    - Return all the information for out company benefits.

    ** Rivals **
    - Turkish Airlines
    - SunExpress
    - Pegasus

    ** Use the tables to display data **
    """,
    tools=[tavily_tools, Crawl4aiTools(max_length=1000), YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    add_history_to_messages=True,
    num_history_responses=2,
    show_tool_calls=True,
    structured_output=True,
    markdown=True,
)

warehouse_agent = Agent(
    name="WarehouseAgent",
    model=bedrock_model,
    role="Warehouse Manager",
    structured_output=True,
    description="""
    You are a team of experts to manage the company. You are responsible for all operations of the company.
    """,
    markdown=True,
    tools=[warehouse_plugin],
    system_prompt="""You are a database assistant that MUST use the provided tools to answer questions.
    Always use the WarehousePlugin tool when querying database information.
    Never try to answer database questions from memory - always query the actual database.
    Check the existing tables and columns before querying the database.
    """,
    instructions="""
    ** Instructions **
    - You are a database assistant that MUST use the provided tools to answer questions.
    - Always use the WarehousePlugin tool when querying database information.
    - Never try to answer database questions from memory - always query the actual database.
    """
)

file_agent = Agent(
    name="FileAgent",
    model=bedrock_model,
    description="""
    You are a computer file operator.
    Your job is to read and write files.
    """,
    role="File Operator",
    instructions=[
        "Read and write files.",
        "If you create file successfully, return the file name to the user.",
        "If you face with an error, return the error to the user.",
    ],
    tools=[FileTools()],
    add_history_to_messages=True,
    num_history_responses=2,
    show_tool_calls=True,
    markdown=True,
    structured_output=True,
)


team = Agent(
    model=bedrock_model,
    description= """
        You are a team of experts about web research, warehouse management, file operations and python programming.
        Your job is to work together to solve the given problem.
    """,
    role="expert team",
    instructions=["If you remember the given task, return your answer from memory",
                  "Return the response of the team to the user",
                  "Return the first response if you are sure about the answer"],
    team=[researcher_agent, python_agent, file_agent, warehouse_agent],
    add_history_to_messages=True,
    num_history_responses=2,
    memory = AgentMemory(
        db=leader_memory
    ),
    storage=leader_storage,
    show_tool_calls=True,
    monitoring=True,
    debug_mode=True,
)

team.cli_app()