# 🤖 Multiagentes

Sistema multiagente construído com [LangGraph](https://github.com/langchain-ai/langgraph) e [LangChain](https://github.com/langchain-ai/langchain), no qual quatro agentes especializados colaboram para responder a uma pergunta do usuário: um **pesquisador**, um **analista**, um **agente de decisão** e um **redator**.

## ⚙️ Como funciona

O fluxo é modelado como um grafo de estados (`StateGraph`) com um **loop condicional de qualidade**: após a análise, um agente de decisão avalia se o conteúdo está completo o suficiente para seguir para a redação final, ou se é necessário pesquisar novamente.

```
START → researcher → analyst → decision ─┬─(APPROVED)─────────→ writer → END
                          ↑               │
                          └─(RESEARCH_AGAIN, se attempts < 2)
```

1. **Researcher (`agents/researcher.py`)**
   Recebe a pergunta do usuário e produz uma pesquisa inicial, levantando os principais conceitos, informações relevantes e pontos que merecem aprofundamento. A cada execução, incrementa o contador `attempts`.

2. **Analyst (`agents/analyst.py`)**
   Recebe a pesquisa produzida pelo agente anterior e faz uma análise crítica: organiza as informações por relevância, aponta limitações e sinaliza o que precisa de mais investigação.

3. **Decision (`agents/decision.py`)**
   Avalia a análise produzida e decide se ela está suficientemente completa, respondendo apenas `APPROVED` ou `RESEARCH_AGAIN`. Essa decisão é usada pelo roteador condicional (`decision_router`) do grafo para definir o próximo passo:
   - `APPROVED` → segue para o **writer**.
   - `RESEARCH_AGAIN` e `attempts < 2` → volta para o **researcher**, gerando uma nova pesquisa.
   - `RESEARCH_AGAIN` com `attempts >= 2` → segue para o **writer** mesmo assim, evitando um loop infinito.

4. **Writer (`agents/writer.py`)**
   Recebe a pesquisa e a análise, e produz a resposta final estruturada (introdução, principais pontos, análise e conclusão) para o usuário.

O estado compartilhado entre os agentes (`AgentState`) contém:

| Campo          | Descrição                                              |
|----------------|-----------------------------------------------------------|
| `question`     | Pergunta original do usuário                            |
| `research`     | Saída do agente pesquisador                             |
| `analysis`     | Saída do agente analista                                |
| `decision`     | Decisão do agente de decisão (`APPROVED` / `RESEARCH_AGAIN`) |
| `attempts`     | Número de vezes que o agente pesquisador foi executado   |
| `final_answer` | Resposta final produzida pelo agente redator             |

## 📁 Estrutura do projeto

```
multiagentes/
├── agents/
│   ├── researcher.py    # Agente pesquisador
│   ├── analyst.py       # Agente analista
│   ├── decision.py      # Agente de decisão (loop de qualidade)
│   └── writer.py        # Agente redator
├── api/
│   └── loginapi.py      # Configuração e autenticação do LLM
├── workflow/
│   └── graph.py         # Definição do grafo (LangGraph)
├── main.py               # Ponto de entrada da aplicação
├── .env                   # Variáveis de ambiente (não versionado)
├── pyproject.toml
└── uv.lock
```

## ✅ Pré-requisitos

- Python 3.10+
- Uma chave de API compatível com a interface da OpenAI (o projeto usa o modelo `gemini-3.1-flash-lite` via `base_url` customizada)
- [uv](https://github.com/astral-sh/uv) **ou** `pip`, para gerenciamento de dependências

## 📦 Instalação

### Usando uv (recomendado)

O projeto já vem com `pyproject.toml` e `uv.lock`, então basta rodar:

```bash
git clone <url-do-repositorio>
cd multiagentes
uv sync
```

### Usando pip

Se preferir usar `pip` em vez de `uv`, crie e ative um ambiente virtual e instale as dependências manualmente:

```bash
git clone <url-do-repositorio>
cd multiagentes

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install langgraph langchain-openai python-dotenv
```

> Como o projeto não possui um `requirements.txt`, as dependências acima foram extraídas dos imports usados no código (`langgraph`, `langchain-openai` e `python-dotenv`). Se preferir, você pode gerar um `requirements.txt` a partir do `pyproject.toml` com `uv export --format requirements-txt > requirements.txt` e então rodar `pip install -r requirements.txt`.

## 🔄 Compatibilidade OpenAI ↔ Gemini

Este projeto usa `ChatOpenAI` (do `langchain-openai`) para se comunicar com o modelo `gemini-3.1-flash-lite`. Isso é possível porque o Google oferece uma **camada de compatibilidade** que permite usar os SDKs oficiais da OpenAI (Python ou TypeScript/JavaScript) para chamar os modelos do Gemini.

Basta apontar a `base_url` para o endpoint do Google e usar sua chave de API do Gemini como `api_key`:

```
base_url=https://generativelanguage.googleapis.com/v1beta/openai/
```

### Como funciona a compatibilidade

- **Endpoints e código**: a estrutura de código padrão da OpenAI (`client.chat.completions.create`) é mantida — só é preciso alterar a URL base e a chave de autenticação.
- **Parâmetros e recursos**: funcionalidades comuns, como streaming de respostas, chamadas de função (*function calling*) e saídas estruturadas em JSON, são mapeadas automaticamente para o padrão do Gemini.
- **Parâmetros específicos (`extra_body`)**: configurações exclusivas do ecossistema do Google (como ferramentas de busca ou níveis avançados de controle de raciocínio) podem ser repassadas usando o argumento `extra_body` nas chamadas da API.

É exatamente esse mecanismo que permite que `api/loginapi.py` use `ChatOpenAI` normalmente, apenas trocando `base_url` e `api_key` para os valores do Gemini.

📚 Saiba mais na [documentação oficial do Gemini API](https://ai.google.dev/gemini-api/docs/openai).

## 🔧 Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
api_key=SUA_CHAVE_DE_API
base_url=URL_BASE_DA_API
```

> As variáveis são carregadas em `api/loginapi.py` através do `python-dotenv`. Se `api_key` não for encontrada, a aplicação lança um erro.

## ▶️ Uso

Edite a pergunta em `main.py`:

```python
question = "O que é educação híbrida?"
```

Execute o projeto:

```bash
# usando uv
uv run main.py

# usando pip (com o venv ativado)
python main.py
```

O terminal exibirá a decisão do agente de qualidade, o número de tentativas de pesquisa realizadas e a resposta final produzida pelo agente redator:

```
===== DECISÃO =====

APPROVED

===== TENTATIVAS =====

1

===== RESPOSTA FINAL =====

<resposta gerada pelos agentes>
```

## 🛠️ Tecnologias utilizadas

- **LangGraph** — orquestração do fluxo entre agentes como um grafo de estados
- **LangChain (langchain-openai)** — integração com o modelo de linguagem
- **python-dotenv** — carregamento de variáveis de ambiente

## 🚀 Possíveis melhorias

- [ ] Adicionar tratamento de erros nas chamadas ao LLM
- [ ] Tornar o limite de tentativas (`attempts >= 2`) configurável
- [ ] Permitir que a pergunta seja informada via linha de comando ou input interativo
- [ ] Adicionar testes automatizados para cada agente
- [ ] Registrar logs intermediários (pesquisa, análise e decisões) em arquivo
- [ ] Suporte a múltiplos modelos/provedores de LLM

## 📄 Licença

Este projeto está sob a licença MIT.

---

## 👨‍💻 Autor

Robert Melo

🔗 LinkedIn: https://www.linkedin.com/in/robertdemelo/ 
🐍 Python | IA | Machine Learning | LangChain | Data Science
