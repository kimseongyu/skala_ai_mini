from typing import Dict, Any, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os
from .base_agent import BaseAgent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from tqdm import tqdm
import time


class ReportGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("report_generator")
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            "CustomTitle", parent=self.styles["Heading1"], fontSize=24, spaceAfter=30
        )
        self.heading_style = ParagraphStyle(
            "CustomHeading", parent=self.styles["Heading2"], fontSize=18, spaceAfter=20
        )
        self.normal_style = self.styles["Normal"]
        self.llm = ChatOpenAI(model="gpt-4")

        # Report generation prompts
        self.overview_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert technology analyst creating executive summaries for technology trend reports.
Your task is to create a concise but comprehensive overview of the technology landscape based on the provided data.

Focus on:
1. Key trends and patterns
2. Most promising technologies
3. Critical risks and opportunities
4. Strategic recommendations

Keep the overview clear, professional, and actionable. Limit to 3-4 paragraphs.""",
                ),
                (
                    "user",
                    """Please create an executive summary based on the following data:

High-Scoring Technologies (score >= 85):
{high_scoring_techs}

Key Metrics Summary:
{metrics_summary}

Critical Risks and Opportunities:
{risk_summary}

Focus on the most significant findings and their implications.""",
                ),
            ]
        )

        self.tech_detail_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert technology analyst creating detailed technology analysis reports.
Your task is to create a comprehensive analysis of a specific technology based on the provided data.

Structure your analysis as follows:
1. Technology Overview (2-3 sentences)
2. Current State and Trends
3. Key Developments and News
4. Risk Analysis
5. Opportunities and Future Outlook
6. Strategic Recommendations

Keep the analysis factual, evidence-based, and actionable.""",
                ),
                (
                    "user",
                    """Please create a detailed analysis for the following technology:

Technology: {tech}

Key Metrics:
{metrics}

Recent News Highlights:
{news_highlights}

Risk Analysis:
{risk_analysis}

Provide a comprehensive analysis focusing on concrete evidence and actionable insights.""",
                ),
            ]
        )

    def save_state(self, state: Dict[str, Any], data: Any) -> None:
        return super().save_state(state, data)

    def prepare_metrics_summary(
        self, trend_metrics: Dict[str, Dict[str, float]]
    ) -> str:
        """Prepare a concise summary of key metrics"""
        summary = []
        for tech, metrics in trend_metrics.items():
            if metrics.get("total_score", 0) >= 85:
                summary.append(f"{tech}:")
                summary.append(
                    f"- Market Adoption: {metrics.get('market_adoption', 0)}"
                )
                summary.append(
                    f"- Research Activity: {metrics.get('research_activity', 0)}"
                )
                summary.append(f"- Total Score: {metrics.get('total_score', 0)}")
                summary.append("")
        return "\n".join(summary)

    def prepare_risk_summary(
        self, risk_analysis: Dict[str, Dict[str, List[Dict[str, str]]]]
    ) -> str:
        """Prepare a concise summary of critical risks and opportunities"""
        summary = []
        for tech, analysis in risk_analysis.items():
            summary.append(f"{tech}:")

            # Add top 2 risks
            risks = analysis.get("risks", [])[:2]
            if risks:
                summary.append("Critical Risks:")
                for risk in risks:
                    summary.append(
                        f"- {risk.get('title', '')}: {risk.get('impact', '')} impact"
                    )

            # Add top 2 opportunities
            opportunities = analysis.get("opportunities", [])[:2]
            if opportunities:
                summary.append("Key Opportunities:")
                for opp in opportunities:
                    summary.append(
                        f"- {opp.get('title', '')}: {opp.get('impact', '')} impact"
                    )
            summary.append("")
        return "\n".join(summary)

    def prepare_news_highlights(
        self, news: List[Dict[str, str]], max_articles: int = 3
    ) -> str:
        """Prepare a concise summary of recent news"""
        highlights = []
        for article in news[:max_articles]:
            highlights.append(f"• {article['title']}")
            highlights.append(f"  {article['summary'][:200]}...")
            highlights.append("")
        return "\n".join(highlights)

    def generate_executive_summary(self, state: Dict[str, Any]) -> str:
        """Generate executive summary using OpenAI"""
        print("\nGenerating Executive Summary...")
        start_time = time.time()

        # Prepare data for the overview
        high_scoring_techs = []
        for tech, metrics in state.get("trend_metrics", {}).items():
            if metrics.get("total_score", 0) >= 85:
                high_scoring_techs.append(tech)

        metrics_summary = self.prepare_metrics_summary(state.get("trend_metrics", {}))
        risk_summary = self.prepare_risk_summary(
            state.get("risk_opportunity_analysis", {})
        )

        # Generate overview
        response = self.llm.invoke(
            self.overview_prompt.format_messages(
                high_scoring_techs="\n".join(high_scoring_techs),
                metrics_summary=metrics_summary,
                risk_summary=risk_summary,
            )
        )

        end_time = time.time()
        print(f"Executive Summary generated in {end_time - start_time:.2f} seconds")
        return response.content

    def generate_tech_analysis(self, tech: str, state: Dict[str, Any]) -> str:
        """Generate detailed analysis for a specific technology"""
        metrics = state.get("trend_metrics", {}).get(tech, {})
        news = state.get("collected_news", {}).get(tech, [])
        risk_analysis = state.get("risk_opportunity_analysis", {}).get(tech, {})

        # Format metrics
        metrics_text = "\n".join(
            [
                f"- {key}: {value}"
                for key, value in metrics.items()
                if key != "total_score"
            ]
        )

        # Format risk analysis
        risk_text = []
        for risk in risk_analysis.get("risks", []):
            risk_text.append(f"• {risk.get('title', '')}")
            risk_text.append(f"  Impact: {risk.get('impact', '')}")
            risk_text.append(f"  {risk.get('explanation', '')}")
        for opp in risk_analysis.get("opportunities", []):
            risk_text.append(f"• {opp.get('title', '')}")
            risk_text.append(f"  Impact: {opp.get('impact', '')}")
            risk_text.append(f"  {opp.get('explanation', '')}")

        # Generate analysis
        response = self.llm.invoke(
            self.tech_detail_prompt.format_messages(
                tech=tech,
                metrics=metrics_text,
                news_highlights=self.prepare_news_highlights(news),
                risk_analysis="\n".join(risk_text),
            )
        )
        return response.content

    def create_technology_section(self, tech: str, data: Dict[str, Any]) -> List:
        """Create a section for a single technology"""
        elements = []

        # Technology title
        elements.append(Paragraph(tech, self.heading_style))

        # Generate detailed analysis
        analysis = self.generate_tech_analysis(tech, data)
        elements.append(Paragraph(analysis, self.normal_style))
        elements.append(Spacer(1, 20))

        # Add metrics table if available
        metrics = data.get("trend_metrics", {}).get(tech, {})
        if metrics:
            elements.append(Paragraph("Key Metrics", self.normal_style))
            metrics_data = [
                ["Metric", "Value"],
                ["Market Adoption", f"{metrics.get('market_adoption', 0)}"],
                ["Research Activity", f"{metrics.get('research_activity', 0)}"],
                ["Investment Interest", f"{metrics.get('investment_interest', 0)}"],
                ["Media Coverage", f"{metrics.get('media_coverage', 0)}"],
                ["Future Potential", f"{metrics.get('future_potential', 0)}"],
                ["Total Score", f"{metrics.get('total_score', 0)}"],
            ]
            t = Table(metrics_data, colWidths=[200, 100])
            t.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 14),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 12),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            elements.append(t)
            elements.append(Spacer(1, 20))

        elements.append(Spacer(1, 30))
        return elements

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final PDF report"""
        print("\nStarting Report Generation...")
        start_time = time.time()

        # Create output directory if it doesn't exist
        os.makedirs("outputs", exist_ok=True)

        # Generate report filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"outputs/tech_trend_report_{timestamp}.pdf"

        # Create the PDF document
        doc = SimpleDocTemplate(report_path, pagesize=letter)
        elements = []

        # Title
        elements.append(Paragraph("Technology Trend Analysis Report", self.title_style))
        elements.append(
            Paragraph(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                self.normal_style,
            )
        )
        elements.append(Spacer(1, 30))

        # Generate and add executive summary
        elements.append(Paragraph("Executive Summary", self.heading_style))
        summary = self.generate_executive_summary(state)
        elements.append(Paragraph(summary, self.normal_style))
        elements.append(Spacer(1, 30))

        # Filter technologies with total score >= 85
        high_scoring_techs = {}
        for keyword, technologies in state["summarized_tech"].items():
            high_scoring_techs[keyword] = []
            for tech in technologies:
                metrics = state.get("trend_metrics", {}).get(tech, {})
                if metrics.get("total_score", 0) >= 85:
                    high_scoring_techs[keyword].append(tech)

        # Process each high-scoring technology
        total_techs = sum(len(techs) for techs in high_scoring_techs.values())
        print(f"\nAnalyzing {total_techs} high-scoring technologies (score >= 85)...")

        with tqdm(total=total_techs, desc="Technology Analysis") as pbar:
            for keyword, technologies in high_scoring_techs.items():
                if (
                    technologies
                ):  # Only add category if it has high-scoring technologies
                    elements.append(
                        Paragraph(f"Category: {keyword}", self.heading_style)
                    )
                    for tech in technologies:
                        elements.extend(self.create_technology_section(tech, state))
                        pbar.update(1)

        print("\nGenerating PDF...")
        # Build the PDF
        doc.build(elements)

        end_time = time.time()
        print(f"\nReport generation completed in {end_time - start_time:.2f} seconds")
        print(f"Report saved to: {report_path}")

        # Update state with report path
        state["full_report"] = report_path
        return state, report_path
