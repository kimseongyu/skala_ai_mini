from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
import json


class TrendPredictorAgent(BaseAgent):
    def __init__(self):
        super().__init__("trend_predictor")
        self.llm = ChatOpenAI(model="gpt-4")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a technology trend analyst. Your task is to analyze the trend of a specific technology based on your knowledge.

Analyze the following aspects and provide numerical scores (0-100):
1. Market Adoption: How widely is this technology being adopted in the industry?
2. Research Activity: How active is the research and development in this area?
3. Investment Interest: How much investment and funding is being directed to this technology?
4. Media Coverage: How much attention is this technology getting in the media?
5. Future Potential: How promising is this technology for future development?

Return ONLY a JSON object with these scores, like this:
{{
    "market_adoption": 85,
    "research_activity": 90,
    "investment_interest": 75,
    "media_coverage": 80,
    "future_potential": 95,
    "total_score": 85
}}

The total_score should be the average of all other scores, rounded to the nearest integer.
Base your analysis on your knowledge of the technology and its current state in the industry.
            """,
                ),
                (
                    "user",
                    "Analyze the trend for this technology: {technology}",
                ),
            ]
        )

    def save_state(self, state: Dict[str, Any], data: Any) -> bool:
        """Save the trend metrics to the state"""
        if data is None:
            return False
        state["trend_metrics"] = data
        return True

    def analyze_trend(self, technology: str) -> Dict[str, float]:
        """Analyze technology trend using OpenAI"""
        try:
            # Get trend analysis from LLM
            message = self.prompt.format_messages(technology=technology)
            response = self.llm.invoke(message)

            # Parse the response to get metrics
            try:
                metrics = json.loads(response.content)
                return metrics
            except json.JSONDecodeError as e:
                print(f"Error parsing LLM response: {e}")
                print(f"Raw response: {response.content}")
                raise

        except Exception as e:
            print(f"Error analyzing trend for {technology}: {e}")
            return {
                "market_adoption": 0,
                "research_activity": 0,
                "investment_interest": 0,
                "media_coverage": 0,
                "future_potential": 0,
                "total_score": 0,
            }

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends for each technology"""
        # Flatten technologies list
        all_technologies = []
        for technologies in state["summarized_tech"].values():
            all_technologies.extend(technologies)

        # Analyze each technology
        trend_metrics = {}
        for tech in all_technologies:
            trend_metrics[tech] = self.analyze_trend(tech)

        # Update state with trend metrics
        state["trend_metrics"] = trend_metrics
        return state, trend_metrics
