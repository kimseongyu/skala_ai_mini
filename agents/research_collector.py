from typing import Dict, Any, List
import arxiv
from datetime import datetime, timedelta
from .base_agent import BaseAgent


class ResearchCollectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("research_collector")

    def save_state(self, state: Dict[str, Any], data: Any) -> None:
        """Save the collected papers to the state"""
        if data is None:
            return False
        state["collected_papers"] = data
        return True

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Collect research papers for each keyword"""
        collected_papers = {}

        for keyword in state["keyword_list"]:
            try:
                # Construct search query
                search = arxiv.Search(
                    query=keyword,
                    max_results=10,
                    sort_by=arxiv.SortCriterion.Relevance,
                    sort_order=arxiv.SortOrder.Descending,
                )

                papers = []
                for result in search.results():
                    # Get paper details
                    paper = {
                        "title": result.title,
                        "summary": result.summary,
                    }

                    # Only include papers from the last 3 years
                    if result.published.year >= datetime.now().year - 3:
                        papers.append(paper)

                collected_papers[keyword] = papers

            except Exception as e:
                print(f"Error processing keyword {keyword}: {e}")
                collected_papers[keyword] = []

        # Update state with collected papers
        state["collected_papers"] = collected_papers
        return state, collected_papers
