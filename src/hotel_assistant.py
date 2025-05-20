from agno.agent import Agent
from agno.tools.sql import SQLTools
from dotenv import load_dotenv 
from textwrap import dedent
from agno.models.groq import Groq
from agno.tools.wikipedia import WikipediaTools
from agno.playground import Playground, serve_playground_app

load_dotenv()


db_url = "postgresql://postgres:09404996869Ye@localhost:2003/postgres"

# SQL Agent
sql_agent = Agent(
    model=Groq(id="llama3-70b-8192"),
    name = "SQL Agent",
    description="You are an agent designed to interact with a SQL database.",
    instructions=dedent("""
    You can order the results by a relevant column to return the most interesting
    examples in the database. Never query for all the columns from a specific table,
    only ask for the relevant columns given the question.

    You MUST double check your query before executing it. If you get an error while
    executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
    database.

    To start you should ALWAYS look at the tables in the database to see what you
    can query. Do NOT skip this step.

    Then you should query the schema of the most relevant tables. 
        - If data is not found, return 'Data not available'.
        
    Always give me with text or markdown.
    """),
    expected_output="Look over the user requirement and patiently say that",
    tools=[SQLTools(db_url=db_url)],
    show_tool_calls=False,
    add_history_to_messages=False,
    markdown=True
)

# Knowledge agent
knowledge_agent = Agent(
    model=Groq(id="llama3-70b-8192"),
    name = "Knowledge Agent",
    tools=[WikipediaTools()],
    description="An expert researcher conducting deep web that are related to Hotel.",
    instructions=dedent("""
        - If the sql_agent does not return useful data, search the information that are related to "Hotel".
        - Ensure accuracy and verify from at least two sources.
        - Return concise but informative summaries.
    """),
    markdown=True,
    show_tool_calls=False,
    add_datetime_to_instructions=True,
)

# Edit agent
editor_agent = Agent(
    model=Groq(id="llama3-70b-8192"),
    name = "Editor Agent",
    description="Combines and polishes content from the SQL and knowledge agents.",
    instructions=dedent("""
        - Merge content from sql_agent and knowledge_agent.
        - Ensure clear, structured, grammatically correct responses.
        - If both agents fail, politely say 'Sorry, I couldn't find the requested information.'
    """),
    markdown=False,
    show_tool_calls=False,
)

# Team
customer_service_team = Agent(
    model=Groq(id="llama3-70b-8192"),
    name="A multi-agent customer service team conducting investigative user requirements collaboratively.",
    role="Executes a structured output and provides it to the customer.",
    team=[sql_agent, knowledge_agent, editor_agent],
    instructions=dedent("""
        You are responsible for producing a well-researched, structured final response based on user queries.
        - First, send the task to the sql_agent.
        - If sql_agent returns 'Data not available' or insufficient data, delegate to knowledge_agent.
        - Then, merge results using editor_agent to generate the final polished response.
        - Finally, present the result to the customer in a clean, friendly format.
    """),
    markdown=False,
    show_tool_calls=False,
    add_datetime_to_instructions=True,
)


app = Playground(agents=[sql_agent, knowledge_agent, editor_agent, customer_service_team]).get_app()

if __name__ == "__main__":
    serve_playground_app("hotel_assistant:app", reload=True)