from typing import Dict, Any, List
from langgraph.graph import Graph
from agents.research_collector import ResearchCollectorAgent
from agents.tech_summarizer import TechSummarizerAgent
from agents.trend_predictor import TrendPredictorAgent
from agents.news_collector import NewsCollectorAgent
from agents.risk_analyzer import RiskAnalyzerAgent
from agents.report_generator import ReportGeneratorAgent


def create_workflow() -> Graph:
    # Initialize agents
    research_collector = ResearchCollectorAgent()
    tech_summarizer = TechSummarizerAgent()
    trend_predictor = TrendPredictorAgent()
    news_collector = NewsCollectorAgent()
    risk_analyzer = RiskAnalyzerAgent()
    report_generator = ReportGeneratorAgent()

    # Create workflow graph
    workflow = Graph()

    # Add nodes
    workflow.add_node("research_collector", research_collector.run)
    workflow.add_node("tech_summarizer", tech_summarizer.run)
    workflow.add_node("trend_predictor", trend_predictor.run)
    workflow.add_node("news_collector", news_collector.run)
    workflow.add_node("risk_analyzer", risk_analyzer.run)
    workflow.add_node("report_generator", report_generator.run)

    # Define edges
    workflow.add_edge("research_collector", "tech_summarizer")
    workflow.add_edge("tech_summarizer", "trend_predictor")
    workflow.add_edge("trend_predictor", "news_collector")
    workflow.add_edge("news_collector", "risk_analyzer")
    workflow.add_edge("risk_analyzer", "report_generator")

    # Set entry point
    workflow.set_entry_point("research_collector")

    return workflow


def run_workflow(keywords: List[str]) -> Dict[str, Any]:
    """Run the complete workflow with given keywords"""
    # Initialize state
    initial_state = {
        "keyword_list": keywords,
        "collected_papers": {},
        "summarized_tech": {},
        "trend_metrics": {},
        "collected_news": {},
        "risk_opportunity_analysis": {},
        "full_report": "",
    }

    # Create and run workflow
    workflow = create_workflow()
    app = workflow.compile()
    final_state = app.invoke(initial_state)

    return final_state
