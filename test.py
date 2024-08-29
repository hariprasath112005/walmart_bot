from typing import Union
from enum import Enum
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from langchain_ollama import OllamaLLM #type: ignore
from langchain_ollama.llms import OllamaLLM # type: ignore
from langchain_core.prompts import ChatPromptTemplate # type: ignore
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse


class Query(BaseModel):
    context: str
    question: str

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")




template = """
You are a friendly chatbot assistant that responds in a conversational
manner to user's questions. Respond in 1-2 complete sentences, unless specifically
asked by the user to elaborate on something. Use History and Context to inform your answers.

Answer the Question below.
Here is the conversation history: {context}

Question :{question}

Answer: 
"""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="gangeshwar/tamil-llama")

chain = prompt | model

@app.get("/")
async def show():
    return FileResponse("static/indexs.html")

@app.post("/chat")
async def handle_conversation(query: Query):
    context = query.context
    question  = query.question

    result = chain.invoke({"context": context, "question": question})
        
    context += f"\nUser: {question}\n AI: {result}"

    return {"answer": result}


    