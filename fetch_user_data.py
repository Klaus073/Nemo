# from database import PostgreSQLConnector
# import asyncio
# import pandas as pd
# import datetime
# from langchain import FAISS
# from langchain.schema import Document
# from typing import List, Dict
# from langchain_community.document_loaders import TextLoader
# import numpy as np
# import os
# import time
# import pickle
# from tqdm import tqdm
# from langchain_community.embeddings import HuggingFaceEmbeddings
# import concurrent.futures

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# async def get_user_data(user_id):
#     db = PostgreSQLConnector()
#     if db.is_connected():
#         print("db connected")
#     # Define your queries for each table
#     queries = {
#         "AppTasks": f"SELECT * FROM \"AppTasks\" WHERE \"CreatorUserId\" = '{user_id}'",
#         "AspNetUsers": f"SELECT * FROM \"AspNetUsers\" WHERE \"Id\" = '{user_id}'",
#         "DiscussionHistories": f"SELECT * FROM \"DiscussionHistories\" WHERE \"UserId\" = '{user_id}'",
#         "Drafts": f"SELECT * FROM \"Drafts\" WHERE \"CreatorUserId\" = '{user_id}'",
#         "Equipments": f"SELECT * FROM \"Equipments\" WHERE \"CreatorUserId\" = '{user_id}'",
#         "Expenses": f"SELECT * FROM \"Expenses\" WHERE \"CreatorUserId\" = '{user_id}'",
#         "Invitations": f"SELECT * FROM \"Invitations\" WHERE \"ReceiverUserId\" = '{user_id}' OR \"SenderUserId\" = '{user_id}'",
#         "Managers": f"SELECT * FROM \"Managers\" WHERE \"UserId\" = '{user_id}'",
#         "Medias": f"SELECT * FROM \"Medias\" WHERE \"UserId\" = '{user_id}'",
#         "Notifications": f"SELECT * FROM \"Notifications\" WHERE \"UserId\" = '{user_id}'",
        
#         "Researches": f"SELECT * FROM \"Researches\" WHERE \"CreatorUserId\" = '{user_id}'",
        
#         "Publications": f"SELECT * FROM \"Publications\" WHERE \"CreatorUserId\" = '{user_id}'",
#     }

#     # Dictionary to store DataFrames for each table
#     dfs = {}

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = {table: asyncio.ensure_future(db.execute_query1(query)) for table, query in queries.items()}
#         for table, future in futures.items():
#             cursor, rows = await future
#             if rows:
#                 columns = [desc[0] for desc in cursor.description]
#                 dfs[table] = pd.DataFrame(rows, columns=columns)

#     return dfs

# async def create_documents_from_df(df: pd.DataFrame) -> list:
#     documents = []

#     def process_row(row):
#         sentence = ', '.join([f"{column}: {value}" for column, value in row.items() if pd.notnull(value)])
#         meta = {column: value for column, value in row.items() if pd.notnull(value)}
#         return Document(page_content=sentence, metadata=meta)

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         document_futures = [executor.submit(process_row, row) for _, row in df.iterrows()]
#         for future in concurrent.futures.as_completed(document_futures):
#             documents.append(future.result())

#     return documents

# async def embedding_pipeline(user_id):
#     docs = []
#     embeddings_dir = f"UserEmbeddingsData/Embeddings_{user_id}"
#     if os.path.exists(embeddings_dir):
#         print(f"Embeddings for user {user_id} already exist. Skipping processing.")
#         return

#     print(f"Embeddings for user {user_id} do not exist. Processing .....")
#     user_data = await get_user_data(user_id)

#     # async with tqdm(total=len(user_data), desc='Processing DataFrames') as pbar:
#     #     for table, df in user_data.items():
#     #         await asyncio.sleep(0)  # To allow other tasks to run
#     #         await create_documents_from_df(df)
#     #         pbar.update(1)

#     for table, df in user_data.items():
#         docs = await create_documents_from_df(df)

#     total_docs = len(docs)
#     if total_docs == 0:
#         status = True
#         return status
#     else:
#          # Save the embeddings
#         db =  FAISS.from_documents(docs, embeddings)
#         status = False
#         return db , status 


#     # Perform CPU-bound operations asynchronously if possible

   
    
    
#     # db.save_local(embeddings_dir)

# # zz = get_user_data("52700585-5642-4366-aded-a9896af705b9")

# # print(len(zz))