from typing import TypedDict, List, Dict
from datetime import datetime


class State(TypedDict):
    # [User Input] 사용자가 정의한 기술 키워드
    keyword_list: List[str]

    # [Agent A - ResearchCollectorAgent] - 키워드별 수집된 논문 데이터
    collected_papers: Dict[str, List[Dict[str, str]]]

    # [Agent B - TechSummarizerAgent] - 키워드별 핵심 기술 요약 결과
    summarized_tech: Dict[str, List[str]]

    # [Agent C - TrendPredictorAgent] - 핵심 기술별 트렌드 분석 정보
    trend_metrics: Dict[str, Dict[str, float]]

    # [Agent D - NewsCollectorAgent] - 핵심 기술별 수집된 뉴스 데이터
    collected_news: Dict[str, List[Dict[str, str]]]

    # [Agent E - RiskOpportunityAnalyzerAgent] - 핵심 기술별 리스크 및 기회 분석
    risk_opportunity_analysis: Dict[str, Dict[str, List[str]]]

    # [Agent F - ReportGeneratorAgent] - 전체 결과를 종합한 PDF 보고서 경로
    full_report: str


class AgentOutput(TypedDict):
    data: dict
    timestamp: str
    agent_name: str
