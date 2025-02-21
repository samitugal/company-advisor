import os

from dotenv import load_dotenv
from phi.agent import Agent, AgentMemory, RunResponse
from phi.memory.classifier import MemoryClassifier
from phi.memory.db.sqlite import SqliteMemoryDb
from phi.memory.summarizer import MemorySummarizer
from phi.model.google import Gemini
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.tools.file import FileTools
from phi.tools.tavily import TavilyTools

from src.plugins import WarehousePlugin

load_dotenv()

tavily_tools = TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))
warehouse_plugin = WarehousePlugin(format_type="markdown")

gemini_model = Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))

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
        db=SqliteMemoryDb(db_file=db_file),
        create_user_memories=True,
        create_session_summary=True,
        summarizer=MemorySummarizer(model=gemini_model),
        classifier=MemoryClassifier(model=gemini_model),
        update_user_memories_after_run=True,
        create_user_memories=True,
        create_session_summary=True,
    )


researcher_agent = Agent(
    name="ResearcherAgent",
    model=gemini_model,
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

    """,
    tools=[tavily_tools, Crawl4aiTools(max_length=1000)],
    add_history_to_messages=True,
    num_history_responses=2,
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    debug_mode=True,
)

warehouse_agent = Agent(
    name="WarehouseAgent",
    model=gemini_model,
    role="Warehouse Manager",
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
    """,
    monitoring=True,
    debug_mode=True,
)

file_agent = Agent(
    name="FileAgent",
    model=gemini_model,
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
    monitoring=True,
    debug_mode=True,
)

agent = Agent(
    name="ManagerAgent",
    model=gemini_model,
    markdown=True,
    team=[warehouse_agent, file_agent, researcher_agent],
    storage=leader_storage,
    system_prompt="""
    You are a company advisor with companion agents. Help the manager to manage the company.
    Do not try to answer question like I can not answer that, use the teams I provided to answer the question.
    You can use the WarehouseAgent to get information about the database. You have all authority to make decisions.
    """,
    show_tool_calls=True,
    update_knowledge=True,
    add_chat_history_to_messages=True,
    num_history_responses=3,
    memory=generate_memory_db(db_file="db/manager_memory.db"),
    instructions="""
    ** Instructions **
    You are a helpful assistant to manage my company. You can track the inventory, sales, and other metrics.
    You can check trending products to sale or financial statues of our rivals.
    You can also check the customers and their preferences.

    ** Team **
    - WarehouseAgent: Use for ALL database queries and information. It has access to the database.
    - FileAgent: Use for file operations. It has access to the file system.
    
    ** Tools **
    - TavilyTools: Use for web searches when needed

    ** Company Rivals **
    - Turkish Airlines
    - SunExpress
    - Pegasus

    ** Behavior **
    - Please be gentle and helpful. You are talking with the manager of the company.
    - Explain your actions and thoughts in detail.
    """,
    monitoring=True,
    debug_mode=True,
)

agent.cli_app(markdown=True)
