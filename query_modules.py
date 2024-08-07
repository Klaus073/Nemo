import asyncio
from database import PostgreSQLConnector
import pandas as pd
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = PostgreSQLConnector()


async def get_data_from_AppTasks(user_id):
    df = pd.DataFrame()
    documents = []

    query = f"SELECT * FROM \"AppTasks\" WHERE \"CreatorUserId\" = '{user_id}'"
    cursor , rows = await db.execute_query1(query)
    if rows:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

    for index, row in df.iterrows():
        sentence = ''. join(f"The app Task title = '{row['Title']}' having description = '{row['Description']}' with Priority = '{row['Priority']}' starts on '{row['StartDate']}' and ends on '{row['EndDate']}' with Research ID '{row['ResearchId']}' which is also updated on '{row['UpdatedAt']}'")
        documents.append(Document(page_content=sentence))
    
    return documents

async def get_data_from_AspNetUsers(user_id):
    df = pd.DataFrame()
    documents = []

    query =f"SELECT * FROM \"AspNetUsers\" WHERE \"Id\" = '{user_id}'"
    cursor , rows = await db.execute_query1(query)
    if rows:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

    for index, row in df.iterrows():
        sentence = ''. join(f"The user's profile contains the following information (My Name): First Name: '{row['FirstName']}' Last Name: '{row['LastName']}' Email: '{row['Email']}' Institution: '{row['Institution']}' Degree: '{row['Degree']}' Major: '{row['Major']}' Joined Date: '{row['JoinedDate']}' University Name: '{row['University']}' Address: '{row['AddressLine1']} {row['AddressLine2']}' Role: '{row['Role']}' Username: '{row['UserName']}' Email: '{row['Email']}'.")
        documents.append(Document(page_content=sentence))
    
    return documents

async def get_data_from_Equipments(user_id):
    df = pd.DataFrame()
    documents = []

    query = f"SELECT * FROM \"Equipments\" WHERE \"CreatorUserId\" = '{user_id}'"
    cursor , rows = await db.execute_query1(query)
    if rows:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

    for index, row in df.iterrows():
        sentence = ''. join(f"The equipment titled '{row['Title']}' has a description of '{row['Description']}', manufactured by '{row['Manufacturer']}' with model '{row['Model']}'. It is assigned to Technician '{row['TechnicianName']}' whose email is '{row['TechnicianEmail']}' and phone number is '{row['TechnicianPhone']}'.")
        documents.append(Document(page_content=sentence))
    
    return documents

async def get_data_from_Expenses(user_id):
    df = pd.DataFrame()
    documents = []

    query = f"SELECT * FROM \"Expenses\" WHERE \"CreatorUserId\" = '{user_id}'"
    cursor , rows = await db.execute_query1(query)
    if rows:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

    for index, row in df.iterrows():
        sentence = ''. join(f"For expenses, the title '{row['Title']}' describes '{row['Description']}' with an amount of '{row['Amount']}', and it's marked as '{row['Status']}'.")
        documents.append(Document(page_content=sentence))
    
    return documents

async def get_data_from_Invitations(user_id):
    df = pd.DataFrame()
    documents = []

    query = f"SELECT * FROM \"Invitations\" WHERE \"ReceiverUserId\" = '{user_id}'"
    cursor , rows = await db.execute_query1(query)
    if rows:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

    for index, row in df.iterrows():
        sentence = ''. join(f"For invitations, the note '{row['InvitationNote']}' was created at '{row['CreatedAt']}'.")
        documents.append(Document(page_content=sentence))
    
    return documents

async def get_data_from_Managers(user_id):
    df = pd.DataFrame()
    documents = []

    query = f"SELECT * FROM \"Managers\" WHERE \"UserId\" = '{user_id}'"
    cursor , rows = await db.execute_query1(query)
    if rows:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

    for index, row in df.iterrows():
        sentence = ''. join(f"For managers, the user with email '{row['UserEmail']}' and Mangager name '{row['UserFirstName']}' '{row['UserLastName']}' is assigned to team ID '{row['TeamId']}'.")
        documents.append(Document(page_content=sentence))
    
    return documents

async def get_data_from_Notifications(user_id):
    df = pd.DataFrame()
    documents = []

    query = f"SELECT * FROM \"Notifications\" WHERE \"UserId\" = '{user_id}'"
    cursor , rows = await db.execute_query1(query)
    if rows:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

    for index, row in df.iterrows():
        sentence = ''. join(f"For notifications, the message '{row['Message']}' with title '{row['Title']}' was created at '{row['CreatedAt']}'.")
        documents.append(Document(page_content=sentence))
    
    return documents

async def get_data_from_Researches(user_id):
    df = pd.DataFrame()
    documents = []

    query = f"SELECT * FROM \"Researches\" WHERE \"CreatorUserId\" = '{user_id}'"
    cursor , rows = await db.execute_query1(query)
    if rows:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

    for index, row in df.iterrows():
        sentence = ''. join(f"For researches, the project/research titled '{row['Title']}' was created at '{row['CreatedAt']}' with the description '{row['Description']}'. It has a priority of '{row['Priority']}', starting on '{row['StartDate']}' and ending on '{row['EndDate']}'. The current status is '{row['Status']}'.")
        documents.append(Document(page_content=sentence))
    
    return documents

async def get_data_from_Publications(user_id):
    df = pd.DataFrame()
    documents = []

    query = f"SELECT * FROM \"Publications\" WHERE \"CreatorUserId\" = '{user_id}'"
    cursor , rows = await db.execute_query1(query)
    if rows:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

    for index, row in df.iterrows():
        sentence = ''. join(f"For publications, the item named '{row['Name']}' was created at '{row['CreatedAt']}' and is scheduled to start on '{row['StartDate']}' with a priority of '{row['Priority']}'. Its current status is '{row['Status']}'.")
        documents.append(Document(page_content=sentence))
    
    return documents



async def embedding_pipeline(user_id):

    docs = []
    print("got here")
    tasks = await get_data_from_AppTasks(user_id)
    users = await get_data_from_AspNetUsers(user_id)
    equipoment = await get_data_from_Equipments(user_id)
    expenses = await get_data_from_Expenses(user_id)
    invitations = await get_data_from_Invitations(user_id)
    managers = await get_data_from_Managers(user_id)
    notifications = await get_data_from_Notifications(user_id)
    researches = await get_data_from_Researches(user_id)
    publications = await get_data_from_Publications(user_id)

    docs = tasks + users + equipoment + expenses + invitations + managers + notifications + researches + publications
    
    total_docs = len(docs)
    if total_docs == 0:
        status = True
        return status
    else:
         # Save the embeddings
        db =  FAISS.from_documents(docs, embeddings)
        status = False
        return db , status

   

# Run the async function
# asyncio.run(embedding_pipeline("52700585-5642-4366-aded-a9896af705b9"))
