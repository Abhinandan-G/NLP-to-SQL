#NLP - SQL
from crewai import Agent, Task, Process, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
import mysql.connector as sql
import json
api_key = "paste the api key here"

nlp = input("How can i help?: ")

agent_nlp_sql = Agent(
    role = 'NLP to SQL converter',
    goal = 'Generate Natural language to sql queries from the given input',
    backstory = 'You are a Database Engineer who is well versed in understanding natural languages and converting them into SQL queries.',
    verbose =False,
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",verbose=True,temperature=0.1, google_api_key=api_key
    )
)

nlp_task = Task(
    description = f"generate SQL query based on the input from the user and make sure the query is accurate, here's the query : {nlp}",
    agent = agent_nlp_sql,
    expected_output="Generated SQL query"
)

crew = Crew(
    agents = [agent_nlp_sql],
    tasks = [nlp_task],
    verbose = False,
)

op = crew.kickoff()

# print(type(op))
print(op)

cnx=sql.connect(host='127.0.0.1',user='your username',password='your password',database='name of the database')

if(cnx.is_connected()):
    print("connected")
else:
    print("not connected")

curs=cnx.cursor()

curs.execute(op)

result=curs.fetchall()
json_results = json.dumps(result)
# print(json_results)
# print(type(json_results))

for i in json_results:
    if(i==']'):
        print(i)
        print()
    else:
        print(i,end="")


cnx.commit()
cnx.close()
