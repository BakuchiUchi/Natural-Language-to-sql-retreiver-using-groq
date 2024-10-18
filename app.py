from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
import psycopg2
import streamlit as st
import os
from llama_index.llms.groq import Groq
from llama_index.core.llms import ChatMessage

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

conn = psycopg2.connect(database="EMPLOYEE",
                        host="localhost",
                        user="postgres",
                        password="admin",
                        port="5432")
''''''
## load the GROQ And OpenAI API KEY 
groq_api_key=os.getenv('GROQ_API_KEY')


llm = Groq(model="Llama-3.1-70b-versatile", api_key=groq_api_key) #llama3-70b-8192

prompt1 = '''You are a expert at converting natural laguage to sql commands
        \n the SQL database has the name emp and has the following columns - EMPNO (means employee number), ENAME(emloyee name), 
    JOB(telling what job that partivular employee has), MGR(some random collumn with number), HIREDATE(date on which employee was hired),SAL(Salary of the employee), C0MM, DPTNO(dapartment no.) \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM emp ;
    \nExample 2 -, 
    the SQL command will be something like this SELECT * FROM emp 
    where "DEPTNO" = 20; 
    also the sql code should not have ``` in beginning or end and sql word in output also column should be in inverveted comma's when refrencing in code \n this is wrong :FROM emp WHERE HIREDATE > '1981-12-31' 
    \n this is right way SELECT * FROM emp WHERE "HIREDATE" > '1981-12-31' ''' 

def getresp1(ques,prompt):
    messages = [ChatMessage( role="system", content= prompt ),
    ChatMessage(role="user", content=ques), ]
    resp = llm.chat(messages)
    resp= str(resp)
    reply=resp[11:]
    return(reply)
def getresp2(ques,prompt):
    messages = [ChatMessage( role="system", content= prompt ),
    ChatMessage(role="user", content=ques), ]
    resp = llm.chat(messages)
    resp= str(resp)
    reply=resp[11:]
    return(reply)


def read_sql_query(sql):
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt2= '''you are a expert in converting SQL queries results to Natural Language and you are vey good at presenting them in a tabular way \n and make sure they are horizontal tabular ''' 


if submit:
    response=getresp1(question,prompt1)
    print(response)
    response=read_sql_query(response)
    st.subheader("The Requested Information is as follows: ")
    resp2= str(response)
    resp2=getresp2(resp2,prompt2)
    st.header(resp2)


