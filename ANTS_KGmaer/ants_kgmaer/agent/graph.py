"""LangGraph orchestration of the same tested retrieval and classification steps."""

from typing import TypedDict


class GraphState(TypedDict, total=False):
    rounds: int
    retrieval_done: bool
    result: dict


def execute_graph(session):
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError:
        raise RuntimeError("Install ANTS_KGmaer[agent] to use the LangGraph orchestrator") from None

    def retrieve(state):
        session.retrieve_once()
        return {"rounds": session.rounds, "retrieval_done": session.retrieval_done}

    def route(state):
        return "classify" if state["retrieval_done"] or state["rounds"] >= 2 else "retrieve"

    def classify(state):
        return {"result": session.classify()}

    graph = StateGraph(GraphState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("classify", classify)
    graph.add_conditional_edges(START, route, {"retrieve": "retrieve", "classify": "classify"})
    graph.add_conditional_edges("retrieve", route, {"retrieve": "retrieve", "classify": "classify"})
    graph.add_edge("classify", END)
    return graph.compile().invoke({"rounds": session.rounds, "retrieval_done": session.retrieval_done},
                                  {"recursion_limit": 8})["result"]
