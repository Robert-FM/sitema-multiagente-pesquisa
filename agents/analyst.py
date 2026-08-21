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

def analyst(research: str) -> str:
    prompt = f"""
Você é um agente especialista em análise.

Você recebeu uma pesquisa produzida por outro agente.

Sua tarefa é analisar criticamente essa pesquisa.

Pesquisa recebida:
{research}

Faça:

1. Identifique os pontos mais importantes.
2. Organize as informações por relevância.
3. Identifique possíveis problemas ou limitações.
4. Destaque informações que precisam de maior investigação.
5. Apresente uma conclusão da sua análise.

Não invente informações que não estejam presentes na pesquisa.
"""

    response = llm.invoke(prompt)

    return response.content