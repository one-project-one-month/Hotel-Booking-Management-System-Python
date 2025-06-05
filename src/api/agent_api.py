from langchain_groq import ChatGroq
from dotenv import load_dotenv 
import os  
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
langchain_key = os.getenv("LANGCHAIN_API_KEY")# type: ignore
if not langchain_key:
    raise ValueError("LANGCHAIN_API_KEY environment variable is not set.")

os.environ["LANGCHAIN_API_KEY"] = langchain_key

db_uri = os.getenv("DATABASE_URL")
model = ChatGroq(model_name="llama-3.3-70b-versatile") # type: ignore


if db_uri is None:
    raise ValueError("DATABASE_URL environment variable is not set.")
db = SQLDatabase.from_uri(db_uri)
#print(db.dialect) -> postgresql


toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

system_message = """
You are an agent designed to interact with a postgresql database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

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

If you dont know the answer, dont give him the answer say politely that you dont know the answer.
DO NOT mention about the database.
""".format(
    dialect="postgresql",
    top_k=5,
)

memory = MemorySaver()

agent_executor = create_react_agent(model, tools, prompt=system_message, checkpointer=memory)

config = {"configurable": {"thread_id": "user123"}}

prompt_template = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a helpful, friendly assistant who responds naturally and clearly. "
     "You adapt your tone to the user's input: summarize lists, provide explanations, or fulfill requests. "
     "Avoid sounding robotic or overly formal. Use plain language. "
     "**Do not ask any follow-up questions.** "
     "Just provide the most relevant, human-like response to the user's input."),
    
    ("human", "{input}")
])

chain = prompt_template | model

#-----------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class InputQuery(BaseModel):
    query: str

@app.post("/generate")
def generate(input: InputQuery):
    result = agent_executor.invoke({"messages": ("user", input.query)},config) # type: ignore
    output_ = chain.invoke(result['messages'][-1].content)
    return output_.content

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)