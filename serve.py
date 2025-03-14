from typing import List

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langserve import add_routes

# Test LLM
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv(override=True)

# 1. Create prompt template
# system_template = "Translate the following into {language}:"
# prompt_template = ChatPromptTemplate.from_messages([
#     ('system', system_template),
#     ('user', '{text}')
# ])

prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="ให้คำอธิบายสั่นสั้นๆเกี่ยวกับ {topic}."
)

# 2. Create model
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | llm | parser

# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)