from fastapi import FastAPI, HTTPException, BackgroundTasks

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from query_modules import embedding_pipeline
from fastapi.responses import JSONResponse
from chatbot import main_input
import uvicorn
import asyncio

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

embeddings_sessions = {}


# Function to process messages asynchronously
async def process_message(message, user_id):
    
    print(f"{datetime.now()} - Processing message for user {user_id}")
    if f"{user_id}" not in embeddings_sessions:

        result  = await embedding_pipeline(user_id)
        if isinstance(result, tuple):
            db, status = result
            embeddings_sessions[f"{user_id}"] = db
            # retriever = db.as_retriever()
            # docs = retriever.invoke(message)
            # print("Docs : ",docs)
            final = await main_input(message, user_id , db)

        elif result:  
            final = "Sorry! But there is no data for you in the Database."

        else:
            final = "Sorry! But there is no data for you in the Database."

    else:
        logger.info("dictionary : ",embeddings_sessions)
        db = embeddings_sessions[f"{user_id}"]
        # retriever = db.as_retriever()
        # docs = retriever.invoke(message)
        # print("Docs : ",docs)
        final = await main_input(message, user_id , db)

    return final

@app.post('/process')
async def receive_message(message_body: dict):

    message = message_body.get('message')
    user_id = message_body.get('user_id')

    print(f"Req from USer : {user_id} Recieved with message : {message}")

    if not message or not user_id:
        raise HTTPException(status_code=400, detail="Missing message or user_id")

    # Submit the task to the thread pool for parallel execution
    with ThreadPoolExecutor() as executor:
        task = executor.submit(asyncio.run, process_message(message, user_id))
        final = await asyncio.get_event_loop().run_in_executor(None, task.result)

    return JSONResponse(final)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
