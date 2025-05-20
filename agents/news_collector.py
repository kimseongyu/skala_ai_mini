from typing import Dict, Any, List
from datetime import datetime, timedelta
import os
import asyncio
from tavily import AsyncTavilyClient
from .base_agent import BaseAgent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class NewsCollectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("news_collector")
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set")
        self.async_client = AsyncTavilyClient(api_key=self.api_key)
        self.llm = ChatOpenAI(model="gpt-4")
        self.summary_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a news summarizer. Your task is to create a concise and informative summary of a news article.
Focus on the key points, main developments, and important implications.
Keep the summary clear and professional, avoiding unnecessary details.

Return a summary that:
1. Captures the main story and key developments
2. Highlights important implications or impacts
3. Is concise (2-3 sentences)
4. Maintains factual accuracy
""",
                ),
                ("user", "Please summarize this news article:\n\n{article_content}"),
            ]
        )

    def save_state(self, state: Dict[str, Any], data: Any) -> bool:
        """Save the news results to the state"""
        if data is None:
            return False
        state["collected_news"] = data
        return True

    def summarize_article(self, content: str) -> str:
        """Summarize article content using GPT"""
        try:
            message = self.summary_prompt.format_messages(article_content=content)
            response = self.llm.invoke(message)
            return response.content.strip()
        except Exception as e:
            print(f"Error summarizing article: {e}")
            return content[:500] + "..."  # Fallback to truncated content

    async def search_news_for_tech(self, tech: str) -> List[Dict[str, str]]:
        """Search news for a specific technology using Tavily API"""
        try:
            response = await self.async_client.search(
                query=f"{tech} technology news",
                max_results=10,
                topic="news",
                days=365 * 3,  # Last 3 years
                include_images=True,
                include_raw_content=True,
            )

            articles = []
            for i, result in enumerate(response["results"]):
                raw_content = result.get("raw_content", "")
                summary = self.summarize_article(raw_content)

                article = {"title": result["title"], "summary": summary}
                articles.append(article)

            return articles
        except Exception as e:
            print(f"Error searching news for {tech}: {e}")
            return []

    async def collect_news_async(
        self, technologies: List[str]
    ) -> Dict[str, List[Dict[str, str]]]:
        """Collect news for multiple technologies asynchronously"""
        tasks = [self.search_news_for_tech(tech) for tech in technologies]
        results = await asyncio.gather(*tasks)
        return dict(zip(technologies, results))

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Collect news articles for technologies with total_score >= 85"""
        # Get technologies with total_score >= 85
        high_score_techs = []
        for tech, metrics in state.get("trend_metrics", {}).items():
            if metrics.get("total_score", 0) >= 85:
                high_score_techs.append(tech)
                print(
                    f"Collecting news for high-scoring technology: {tech} (score: {metrics['total_score']})"
                )

        if not high_score_techs:
            print("No technologies found with total_score >= 85")
            state["collected_news"] = {}
            return state, {}

        # Run async collection for high-scoring technologies
        loop = asyncio.get_event_loop()
        news_results = loop.run_until_complete(
            self.collect_news_async(high_score_techs)
        )

        # Update state with collected news
        state["collected_news"] = news_results
        return state, news_results
