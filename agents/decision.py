from api.loginapi import carregar_api

llm = carregar_api()


def decision_agent(analysis: str) -> str:
    prompt = f"""
Você é um agente responsável por decidir se uma análise
está suficientemente completa para gerar uma resposta final.

Analise o conteúdo abaixo:

{analysis}

Responda SOMENTE com uma das duas opções:

APPROVED
RESEARCH_AGAIN

Use:

APPROVED
quando a análise estiver suficientemente clara e completa.

RESEARCH_AGAIN
quando a análise estiver incompleta, superficial ou precisar
de mais informações.
"""

    response = llm.invoke(prompt)

    return response.content.strip()