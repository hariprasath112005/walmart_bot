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
You are a friendly walmart chatbot assistant that responds in a conversational
manner to user's questions. Respond in 1-2 complete sentences, unless specifically
asked by the user to elaborate on something. Use History and Context to inform your answers.

Only answer questions related to Walmart or any enquiries and also you can answer some basic questions about yourself. If a question is not related to Walmart, 
respond with: "I'm sorry, I can only answer questions related to Walmart.

Answer the Question below.
Here is the conversation history: {context}

Question :{question}

Answer: 
"""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama2")

chain = prompt | model

#walmart_keywords = ["Walmart", "store", "order", "return", "product", "shipping", "payment"]

#def is_related_to_walmart(question):
#    return any(keyword.lower() in question.lower() for keyword in walmart_keywords)

@app.get("/")
async def show():
    return FileResponse("static/indexs.html")

@app.post("/chat")
async def handle_conversation(query: Query):
    context = query.context
    question  = query.question

    result = chain.invoke({"context": context, "question": question})

    #if not is_related_to_walmart(result):
     #   result = "I'm sorry, I can only answer questions related to Walmart."

        
    context += f"\nUser: {question}\n AI: {result}"

    return {"answer": result}

    
