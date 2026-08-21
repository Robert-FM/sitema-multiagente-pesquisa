from api.loginapi import carregar_api

llm = carregar_api()

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