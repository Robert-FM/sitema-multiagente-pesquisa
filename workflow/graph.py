from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.researcher import researcher
from agents.analyst import analyst
from agents.writer import writer
from agents.decision import decision_agent


class AgentState(TypedDict):
    question: str
    research: str
    analysis: str
    decision: str
    attempts: int
    final_answer: str


def researcher_node(state: AgentState):
    research = researcher(state["question"])

    return {
        "research": research,
        "attempts": state["attempts"] + 1
    }


def analyst_node(state: AgentState):
    analysis = analyst(state["research"])

    return {
        "analysis": analysis
    }


def decision_node(state: AgentState):
    decision = decision_agent(state["analysis"])

    return {
        "decision": decision
    }


def writer_node(state: AgentState):
    final_answer = writer(
        state["research"],
        state["analysis"]
    )

    return {
        "final_answer": final_answer
    }


def decision_router(state: AgentState):

    decision = state["decision"]
    attempts = state["attempts"]

    if decision == "APPROVED":
        return "writer"

    if attempts >= 2:
        return "writer"

    return "researcher"


workflow = StateGraph(AgentState)


workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("decision", decision_node)
workflow.add_node("writer", writer_node)


workflow.add_edge(START, "researcher")

workflow.add_edge("researcher", "analyst")

workflow.add_edge("analyst", "decision")


workflow.add_conditional_edges(
    "decision",
    decision_router,
    {
        "writer": "writer",
        "researcher": "researcher",
    }
)


workflow.add_edge("writer", END)


graph = workflow.compile()