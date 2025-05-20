from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from .base_agent import BaseAgent


class RiskAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__("risk_analyzer")
        self.llm = ChatOpenAI(model="gpt-4")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert technology risk analyst specializing in identifying risks and opportunities from news articles and market trends.

Your task is to analyze the collected news articles for a specific technology and provide a comprehensive analysis of risks and opportunities.

For each risk and opportunity, provide:
1. A clear, concise title
2. A detailed explanation (2-3 sentences)
3. Supporting evidence from the news articles
4. Potential impact level (High/Medium/Low)
5. Time horizon (Short-term/Medium-term/Long-term)

Format your response exactly like this:

RISKS:
1. [Risk Title]
   - Explanation: [Detailed explanation]
   - Evidence: [Quote or reference from news]
   - Impact: [High/Medium/Low]
   - Time Horizon: [Short-term/Medium-term/Long-term]

2. [Next Risk...]

OPPORTUNITIES:
1. [Opportunity Title]
   - Explanation: [Detailed explanation]
   - Evidence: [Quote or reference from news]
   - Impact: [High/Medium/Low]
   - Time Horizon: [Short-term/Medium-term/Long-term]

2. [Next Opportunity...]

Focus on concrete evidence from the news articles and avoid speculation. If there's insufficient information for a particular aspect, indicate that clearly.""",
                ),
                (
                    "user",
                    """Analyze the following technology and its news coverage:

Technology: {tech}

News Articles:
{news}

Provide a detailed analysis of risks and opportunities based on the news coverage.""",
                ),
            ]
        )

    def save_state(self, state: Dict[str, Any], data: Any) -> bool:
        """Save the risk analysis to the state"""
        if data is None:
            return False
        state["risk_opportunity_analysis"] = data
        return True

    def parse_analysis(self, content: str) -> Dict[str, List[Dict[str, str]]]:
        """Parse the LLM response into structured risk and opportunity data"""
        risks = []
        opportunities = []
        current_section = None
        current_item = None

        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue

            if "RISKS:" in line:
                current_section = "risks"
                continue
            elif "OPPORTUNITIES:" in line:
                current_section = "opportunities"
                continue

            if line[0].isdigit() and "." in line:
                if current_item:
                    if current_section == "risks":
                        risks.append(current_item)
                    else:
                        opportunities.append(current_item)
                current_item = {"title": line.split(".", 1)[1].strip()}
            elif current_item and line.startswith("- "):
                key, value = line[2:].split(":", 1)
                current_item[key.lower()] = value.strip()

        # Add the last item
        if current_item:
            if current_section == "risks":
                risks.append(current_item)
            else:
                opportunities.append(current_item)

        return {"risks": risks, "opportunities": opportunities}

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risks and opportunities for each technology based on news"""
        risk_opportunity_analysis = {}

        for tech, news in state["collected_news"].items():
            # Format news articles for the prompt
            news_text = "\n\n".join(
                [
                    f"Title: {article['title']}\nSummary: {article['summary']}"
                    for article in news
                ]
            )

            # Generate analysis using LLM
            response = self.llm.invoke(
                self.prompt.format_messages(tech=tech, news=news_text)
            )

            # Parse the structured response
            analysis = self.parse_analysis(response.content)
            risk_opportunity_analysis[tech] = analysis

        # Update state with risk analysis
        state["risk_opportunity_analysis"] = risk_opportunity_analysis
        return state, risk_opportunity_analysis
