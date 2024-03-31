from langchain.tools import BaseTool,StructuredTool, tool
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from src.config.database import engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from src.utlis.constants import description as desc
import os



class SQLCustomTool(BaseTool):
    name = "SQL querying tool"
    description = desc

    def _run(self,user_query:str):
        load_dotenv()
        openai_api_key = os.environ['OPENAI_API_KEY']

        template = """

            Based on the table schema below, write a SQL query that would answer the user's question :
            {schema}

            Question : {question}
            SQL Query

            """

        prompt = ChatPromptTemplate.from_template(template=template)
        prompt.format(schema = "my schema",question = "how many users are there")
        db_uri = os.getenv("SAMPLE_DB_URL")

        db = SQLDatabase.from_uri(db_uri)

        def get_schema(_):
          return db.get_table_info()
        get_schema(None)
        llm = ChatOpenAI()

        sql_chain = (
            RunnablePassthrough.assign(schema = get_schema) 
            | prompt
            | llm.bind(stop = "\n SQL Result:")
            | StrOutputParser()
        )

        template = """
            Based on the schema below , question , sql query , and sql response , write a natural language response : {schema}

            Question: {question}
            SQL Query: {query}
            SQL Response: {response}
            """

        prompt = ChatPromptTemplate.from_template(template=template)
        
        def run_query(query):
            return db.run(query)

        full_chain = (
            RunnablePassthrough.assign(query = sql_chain).assign(
                schema = get_schema,
                response = lambda varibales: run_query(varibales["query"])
            )
            | prompt
            | llm
            | StrOutputParser()
        )
        return full_chain.invoke({"question":f"{user_query}"})

        
    
    def _arun(self,query:str):
        raise NotImplementedError("This tool does not support async :")


