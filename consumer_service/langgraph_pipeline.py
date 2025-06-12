from langgraph.graph import Graph
from .agents.event_classifier import EventClassifierAgent
from .agents.anomaly_detector import AnomalyDetectorAgent
from .agents.alert_generator import AlertGeneratorAgent
from .agents.feedback_loop_agent import FeedbackLoopAgent
from .agents.rag_agent import RAGAgent
from .agents.llm_agent import LLMExplainabilityAgent

def build_agent_graph():
    g = Graph()

    # Initialize agents
    classifier_agent = EventClassifierAgent()
    anomaly_detector_agent = AnomalyDetectorAgent()
    rag_agent = RAGAgent(n_results=5, score_threshold=0.3)
    llm_agent = LLMExplainabilityAgent()
    alert_generator_agent = AlertGeneratorAgent()
    feedback_loop_agent = FeedbackLoopAgent()

    # Add nodes
    g.add_node("classifier", classifier_agent)
    g.add_node("anomaly_detector", anomaly_detector_agent)
    g.add_node("rag_agent", rag_agent)
    g.add_node("llm_agent", llm_agent)
    g.add_node("alert_generator", alert_generator_agent)
    g.add_node("feedback_loop", feedback_loop_agent)

    # Add edges
    g.add_edge("__start__", "classifier")
    g.add_edge("classifier", "anomaly_detector")
    g.add_edge("anomaly_detector", "rag_agent")
    g.add_edge("rag_agent", "llm_agent")
    g.add_edge("llm_agent", "alert_generator")
    g.add_edge("alert_generator", "feedback_loop")
    g.add_edge("feedback_loop", "__end__")

    # Compile graph
    executable_graph = g.compile()
    return executable_graph


async def run_agent_pipeline(event):
    executable_graph = build_agent_graph()
    await executable_graph.ainvoke(event)
