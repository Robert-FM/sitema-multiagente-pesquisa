from api.loginapi import carregar_api

llm = carregar_api()


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