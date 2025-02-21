import os 

from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
from phi.tools.tavily import TavilyTools

from dotenv import load_dotenv

from src.plugins import WarehousePlugin

load_dotenv()

tavily_tools = TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))
warehouse_plugin = WarehousePlugin(format_type="markdown")

agent = Agent(
    model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
    markdown=True,
    tools=[tavily_tools, warehouse_plugin],
    system_prompt="""You are a database assistant that MUST use the provided tools to answer questions.
    Always use the WarehousePlugin tool when querying database information.
    Never try to answer database questions from memory - always query the actual database.""",
    show_tool_calls=True,
    update_knowledge=True,
    add_chat_history_to_messages=True,
    instructions="""
    ** Instructions **
    You are a helpful assistant to manage my company. You can track the inventory, sales, and other metrics.
    You can check trending products to sale or financial statues of our rivals.
    You can also check the customers and their preferences.

    ** Tools **
    - WarehousePlugin: Use this for ALL database queries and information
      - get_table_columns(): Get schema information
      - execute_query(): Run SQL queries
      
    - TavilyTools: Use for web searches when needed

    ** Behavior **
    - Please be gentle and helpful. You are talking with the manager of the company.
    - Explain your actions and thoughts in detail.
    """
)

agent.cli_app(markdown=True) 