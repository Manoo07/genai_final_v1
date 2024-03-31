from langchain.tools import BaseTool,StructuredTool, tool
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from src.config.database import engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os



class CSVCustomTool(BaseTool):
    name = "CSV querying tool"
    description = '''
                    use this tool when user want to query on the CSAT resources feedback excel/csv sheet 
                    it consists of the following columns 
                    **Id,
                    **CsatResourcesId,
                    **LineItemOptionsId ,
                        takes the user input as the query to this tool and returns the answer          "'''

    def _run(self,query:str):
        load_dotenv()
        api_key=os.getenv("OPENAI_API_KEY")
        loader = CSVLoader(file_path='src/services/csat_resources_feedback 1.csv')
        # data = loader.load()
        csv_file = 'src/services/csat_resources_feedback 1.csv'
        
        openai = OpenAI(openai_api_key=api_key)
        agent = create_csv_agent(
            openai,
            csv_file,
            verbose=True,
            # agent_type=AgentType.ZERO_SHOT_LEARNING,
            # prompt = prompt  # Use this agent type
        )
        return agent.invoke(query)
    
    
    def _arun(self,query:str):
        raise NotImplementedError("This tool does not support async :")


# @tool
# ""
# def sql_custom_agent(query:str):

#     load_dotenv()
#     api_key=os.getenv("OPENAI_API_KEY")

#     llm = OpenAI(
#         openai_api_key=api_key,
#         temperature=0
#     )
#     db = SQLDatabase(engine)
#     agent = create_sql_agent(   
#         llm=llm,
#         toolkit=SQLDatabaseToolkit(db=db, llm=llm),
#         verbose=True,
#         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         top_k=1000
#         )
#     return agent.run(query)
    