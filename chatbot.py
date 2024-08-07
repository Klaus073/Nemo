
import asyncio
import os
import json
from langchain import FAISS
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from openai import OpenAI
from database import PostgreSQLConnector
from langchain_community.llms import Ollama

from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from langchain.vectorstores.base import VectorStoreRetriever
from langchain.chains import ConversationalRetrievalChain
import datetime
from langchain.memory import ConversationBufferMemory

from langchain_community.embeddings import HuggingFaceEmbeddings



embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def vector_db(user_id):
    db = FAISS.load_local(f"UserEmbeddingsData/Embeddings_{user_id}", embeddings)
    return db




llm = ChatOpenAI(model_name="gpt-3.5-turbo" , api_key=os.environ.get("KAMAL_LLM_OPENAI_API_KEY"))
# llm = Ollama(model="mixtral:8x7b-instruct-v0.1-q5_K_M")
# llm = VLLMOpenAI(
#     openai_api_key="ollama",
#     openai_api_base="https://edc8-38-147-83-11.ngrok-free.app/v1",
#     model_name="mixtral:8x7b-instruct-v0.1-q5_K_M")
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages= True)

# def get_or_create_memory_for_session(session_id):
#     if session_id not in memory_dict:
#         memory_dict[session_id] = ConversationSummaryMemory(llm = llm , memory_key="chat_history", return_messages=True )
#     return memory_dict[session_id]




def chatting(user_input, user_id , db):

    general_system_template = r""" 
                <s>[INS]
  
                **Persona:**
                You are a personal chatbot for the user. All the data in the provided context belongs to the user. The user will be asking questions from his data and will provide a context to find the answer.
                You have to reason for the question from the provided context.

                **Instructions:**
                - You will be given today's date with every question, in case you need today's date for reference then you will use it,
                - While answering the question do not reveal that you reading a provided context.

                question = {question}
                context = {context}

                **Let's tackle this step by step:**

                ### 1. **Determine User Query:**
                - Understand user input and what is human saying.
                - You do not need always to answer from the context.
                - You have to decide whether to answer from the context or on your own.
                
                ### 2. **Contextual Analysis and Justification**
                - Carefully examine the provided context to understand the problem thoroughly
                - Evaluate potential responses to the question based on the information available.
                - Justify the chosen answer by aligning it with the context and supporting it with logical reasoning or evidence.
                - Ensure that the answer addresses the question directly and comprehensively, considering any nuances or complexities present in the context.
                
                ### 3. **No Self-Generated Content:**
                - Strictly adhere to the information provided by the user and the existing context.
                
                ### 4. **Avoid Extraneous Content:**
                - Don't provide unnecessary details or information outside the given context.

                **Output:**
                - Only Answer the most relevant and similar information:

                [/INS]

               
                """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    general_user_template = "Question:```{question}```"
    messages = [
                SystemMessagePromptTemplate.from_template(general_system_template),
                HumanMessagePromptTemplate.from_template(general_user_template)
    ]
    aqa_prompt = ChatPromptTemplate.from_messages( messages )
    retriever = VectorStoreRetriever(vectorstore=db, search_kwargs={"k":8})
    conversation = ConversationalRetrievalChain.from_llm(llm, retriever= retriever, memory= memory , combine_docs_chain_kwargs={"prompt":aqa_prompt}, verbose=False)
    
    conversation.invoke({'question': user_input})
    # print(memory.buffer)
    return memory.buffer[-1].content

def ollama_hosted_llm(question , user_id , db):

    psql =PostgreSQLConnector()
    res = psql.execute_query(f"""SELECT * FROM "AspNetUsers" WHERE "Id" = '{user_id}';""")

    first_name = res[0][1]
    last_name = res[0][2]

    # db = vector_db(user_id)
    retriever = db.as_retriever()
    docs = retriever.invoke(question)

    context = "" 
    for doc in docs:
        context += doc.page_content + "\n"  # Add a newline after each document content

    URL = os.getenv("NGROK_URL")
    client = OpenAI(
                base_url = "https://13b8-104-255-9-187.ngrok-free.app/v1",
                api_key='ollama'
                )

    system =   f"""
                <s>[INS]
  
                Role:
                You are a personal chatbot for the user with First Name: {first_name} Last Name: {last_name}. All the data in the provided context belongs to the user. The user will be asking questions from his own data and will provide a context to find the answer.
                You have to reason for the question from the provided context. Determine wheter to answer from context or your own.

                

                question = {question}
                context = {context}

                **Let's tackle this step by step:**

                ### 1. **Determine User Query:**
                - Understand user input and what is human saying.
                - You do not need always to answer from the context.
                - You have to decide whether to answer from the context or on your own.
                
                ### 2. **Contextual Analysis and Justification**
                - Carefully examine the provided context to understand the problem thoroughly
                - Evaluate potential responses to the question based on the information available.
                - Justify the chosen answer by aligning it with the context and supporting it with logical reasoning or evidence.
                - Ensure that the answer addresses the question directly and comprehensively, considering any nuances or complexities present in the context.
                
                ### 3. **No Self-Generated Content:**
                - Strictly adhere to the information provided by the user and the existing context.
                
                ### 4. **Avoid Extraneous Content:**
                - Don't provide unnecessary details or information outside the given context.

                Output:
                - Only Answer the most relevant and similar information:

                [/INS]

                """

    response = client.chat.completions.create(
                model="mixtral:8x7b-instruct-v0.1-q5_K_M",
                messages=[
                    {"role": "system", "content": f"{system}"},
                    {"role": "user", "content": f"{question}"}
                    
                ]
)
    
    return response.choices[0].message.content
     

def chat(question , user_id , db):

    psql =PostgreSQLConnector()
    res = psql.execute_query(f"""SELECT * FROM "AspNetUsers" WHERE "Id" = '{user_id}';""")

    first_name = res[0][1]
    last_name = res[0][2]

    # db = vector_db(user_id)
    retriever = db.as_retriever()
    docs = retriever.invoke(question)

    context = "" 
    for doc in docs:
        context += doc.page_content + "\n"  # Add a newline after each document content

    prompt = f"""
                <s>[INS]
                <<Role>>

                **Role:**

                - You are the personal AI chatbot assistant for the user.
                - All information within the provided context belongs to the user.
                - The user will be seeking answers and assistance based on their own data.
                - Your primary task is to analyze the given context and decide whether to respond directly from the provided information or to generate a new response autonomously.
                - Your goal is to reason effectively based on the context provided, ensuring that your responses are relevant and helpful to the user's inquiries.

                <</Role>>

                <<Context>>
                context = {context}
                <</Context>>

                <<Instructions>>

                **Let's tackle this step by step:**

                ### 1. **Determine User Query:**
                - Understand user input and what is human saying.
                - You do not need always to answer from the context.
                - You have to decide whether to answer from the context or on your own.
                
                ### 2. **Contextual Analysis and Justification**
                - Carefully examine the provided context to understand the problem thoroughly
                - Evaluate potential responses to the question based on the information available.
                - Justify the chosen answer by aligning it with the context and supporting it with logical reasoning or evidence.
                - Ensure that the answer addresses the question directly and comprehensively, considering any nuances or complexities present in the context.
                
                ### 3. **No Self-Generated Content:**
                - Strictly adhere to the information provided by the user and the existing context.
                
                ### 4. **Avoid Extraneous Content:**
                - Don't provide unnecessary details or information outside the given context.

                <</Instructions>>

                Output:
                - Only Answer the most relevant and similar information:

                [/INS]

                """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    prompt_rough = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )
    conversation = LLMChain(
            llm=llm,
            prompt=prompt_rough,
            verbose=False,
            memory=memory
        )
        
    conversation({"question": question})
    cleaned_query_result = memory.buffer[-1].content.replace('\\', '')
    return cleaned_query_result


async def main_input(user_input, user_id , db):
    output = chat(user_input, user_id , db)
    return output




# q = "tga on cl samples"
# db = vector_db("52700585-5642-4366-aded-a9896af705b9")

# ans = db.similarity_search(q)
# retriever = db.as_retriever()
# docs = retriever.invoke(q)
# print(docs)

# all_docs_content = "" 
# for doc in docs:
#     all_docs_content += doc.page_content + "\n"  # Add a newline after each document content

# # print("Context: ",all_docs_content)
# # print(ans[0].page_content)




# print(explain_query(q,all_docs_content))

# print(ollama_hosted_llm(f"What tasks do I have pending that are assigned to me?: today's date = {datetime.date.today()}" , "52700585-5642-4366-aded-a9896af705b9"))
# print(main_input("what is my name","0"))