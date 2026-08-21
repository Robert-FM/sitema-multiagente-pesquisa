from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

def carregar_api():
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

    return llm