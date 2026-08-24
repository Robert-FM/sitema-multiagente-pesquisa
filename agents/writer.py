from api.loginapi import carregar_api

llm = carregar_api()

def writer(research: str, analysis: str) -> str:
    prompt = f"""
Você é um agente responsável pela redação final.

Você recebeu o trabalho de dois agentes.

PESQUISA:
{research}

ANÁLISE:
{analysis}

Produza uma resposta final clara, objetiva e tecnicamente correta.

REGRAS IMPORTANTES:
- Não altere nomes de tecnologias ou conceitos técnicos.
- Não crie informações que não estejam na pesquisa ou análise.
- Não invente fontes, números ou referências.
- Preserve as siglas técnicas originais.
- Use português do Brasil.
- Não mencione que você é um agente de IA.

Estruture a resposta em:

1. Introdução
2. Principais pontos
3. Análise
4. Conclusão
"""

    response = llm.invoke(prompt)

    return response.content