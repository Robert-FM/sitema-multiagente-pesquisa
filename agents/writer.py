from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

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


def writer(research: str, analysis: str) -> str:
    prompt = f"""
Você é um agente responsável pela redação final.

Você recebeu o trabalho de dois agentes:

PESQUISA:
{research}

ANÁLISE:
{analysis}

Sua tarefa é produzir uma resposta final clara, objetiva e
bem estruturada para o usuário.

Organize a resposta da seguinte maneira:

1. Introdução
2. Principais pontos
3. Análise
4. Conclusão

Utilize somente as informações fornecidas pelos agentes.
Não invente informações.
"""

    response = llm.invoke(prompt)

    return response.content