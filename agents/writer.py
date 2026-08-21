from api.loginapi import carregar_api

llm = carregar_api()

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