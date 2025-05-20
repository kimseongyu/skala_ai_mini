from typing import Dict, Any, List
from .base_agent import BaseAgent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class TechSummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("tech_summarizer")
        self.llm = ChatOpenAI(model="gpt-4")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a technology expert. Your task is to extract ONLY the main technology terms from research papers.
            Rules:
            1. Extract ONLY the main technology terms, one per line
            2. DO NOT include any explanations or descriptions
            3. DO NOT include any punctuation
            4. DO NOT include any numbers or special characters
            5. Each term should be a single word or a short phrase (2-3 words maximum)
            6. Remove any duplicates
            7. Return ONLY the terms, one per line
            
            Example input:
            "This paper discusses the application of machine learning in natural language processing, specifically focusing on transformer architectures and attention mechanisms."
            
            Example output:
            machine learning
            natural language processing
            transformer
            attention mechanism""",
                ),
                (
                    "user",
                    "Extract the main technology terms from these papers:\n{paper_texts}",
                ),
            ]
        )

    def save_state(self, state: Dict[str, Any], data: Any) -> bool:
        """Save the summarized technologies to the state"""
        if data is None:
            return False
        state["summarized_tech"] = data
        return True

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract main technology terms from collected papers"""
        summarized_tech = {}

        for keyword, papers in state["collected_papers"].items():
            try:
                # Combine all paper titles and summaries
                paper_texts = "\n".join(
                    [
                        f"Title: {paper['title']}\nSummary: {paper['summary']}"
                        for paper in papers
                    ]
                )

                # Get technology terms from LLM
                response = self.llm.invoke(
                    self.prompt.format_messages(paper_texts=paper_texts)
                )

                # Process the response to get a list of terms
                terms = [
                    term.strip()
                    for term in response.content.split("\n")
                    if term.strip()
                ]

                # Remove duplicates while preserving order
                unique_terms = list(dict.fromkeys(terms))

                summarized_tech[keyword] = unique_terms

            except Exception as e:
                print(f"Error processing papers for {keyword}: {e}")
                summarized_tech[keyword] = []

        # Update state with summarized technologies
        state["summarized_tech"] = summarized_tech
        return state, summarized_tech
