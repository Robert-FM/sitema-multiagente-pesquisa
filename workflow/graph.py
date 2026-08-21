from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.researcher import researcher
from agents.analyst import analyst
from agents.writer import writer


class AgentState(TypedDict):
    question: str
    research: str
    analysis: str
    final_answer: str


def researcher_node(state: AgentState):
    research = researcher(state["question"])

    return {
        "research": research
    }


def analyst_node(state: AgentState):
    analysis = analyst(state["research"])

    return {
        "analysis": analysis
    }


def writer_node(state: AgentState):
    final_answer = writer(
        state["research"],
        state["analysis"]
    )

    return {
        "final_answer": final_answer
    }


workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("writer", writer_node)


workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)


graph = workflow.compile()