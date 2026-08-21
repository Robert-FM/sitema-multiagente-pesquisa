import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("api_key")
base_url = os.getenv('base_url')

if not api_key:
    raise ValueError(
        "A variável api_key não foi encontrada. "
        "Verifique se ela foi adicionada corretamente ao arquivo .env."
    )


llm = ChatOpenAI(
    model="gemini-3.1-flash-lite",
    api_key=api_key,
    base_url=base_url
)



def researcher(question: str) -> str:
    prompt = f"""
Você é um agente pesquisador.

Sua função é analisar a pergunta abaixo e produzir
uma pesquisa inicial clara e objetiva.

Pergunta:
{question}

Apresente:
1. Os principais conceitos relacionados ao tema.
2. Informações importantes.
3. Possíveis pontos que precisam de uma análise mais aprofundada.

Não invente informações.
"""

    response = llm.invoke(prompt)

    return response.content