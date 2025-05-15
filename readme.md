# AI-Powered Technology Trend Analysis System

본 프로젝트는 AI를 활용하여 미래 기술 트렌드를 분석하고 예측하는 자동화된 시스템입니다.

## Overview

- **Objective**: AI와 데이터 분석을 활용하여 미래 기술 트렌드를 분석하고, 향후 5년 내 주목해야 할 핵심 기술을 도출하여 종합 보고서로 제시합니다.
- **Methods**:
  - 논문 및 뉴스 데이터 자동 수집
  - LLM 기반 기술 요약 및 트렌드 분석
  - 리스크 및 기회 요소 분석
  - 종합 보고서 자동 생성
- **Tools**: LangGraph, OpenAI API, Google Scholar API, Google Trends API

## Features

- **데이터 수집 자동화**

  - 최근 3년간의 주요 기술 키워드 기반 논문 수집 (arXiv API)
  - 관련 뉴스 기사 자동 수집 (Google News API)
  - 기술 트렌드 데이터 수집 (Google Trends API)

- **AI 기반 분석**

  - LLM을 활용한 논문 요약 및 핵심 기술 추출
  - 기술 트렌드 예측 및 점수화
  - 리스크 및 기회 요소 분석

- **보고서 생성**
  - 종합적인 기술 트렌드 분석 보고서 PDF 생성
  - 시각적 데이터 표현 및 메트릭스 포함
  - 실행 가능한 인사이트 및 추천사항 제시

## Tech Stack

| Category  | Details                      |
| --------- | ---------------------------- |
| Framework | LangGraph, LangChain         |
| Language  | Python 3.13                  |
| LLM       | GPT-4 via OpenAI API         |
| Database  | Chroma (Vector DB)           |
| APIs      | Google Scholar, Trends, News |
| PDF       | ReportLab                    |

## Agents

### 1. Research Collector Agent

- arXiv API를 통한 최신 연구 논문 수집
- 키워드 기반 자동 검색 및 필터링
- 논문 메타데이터 추출 (제목, 요약, 저자 등)

### 2. Tech Summarizer Agent

- 수집된 논문의 핵심 기술 추출
- LLM 기반 기술 요약 및 분류
- 기술 간 연관성 분석

### 3. Trend Predictor Agent

- 기술별 트렌드 메트릭스 계산
  - 시장 채택도 (Market Adoption)
  - 연구 활동도 (Research Activity)
  - 투자 관심도 (Investment Interest)
  - 미디어 커버리지 (Media Coverage)
  - 미래 잠재력 (Future Potential)
- 종합 점수 산출 및 순위화

### 4. News Collector Agent

- Google News API를 통한 최신 뉴스 수집
- LLM 기반 뉴스 요약 및 분석
- 기술별 관련성 점수화

### 5. Risk Analyzer Agent

- 수집된 뉴스 기반 리스크 분석
- 기회 요소 식별 및 평가
- 영향도 및 시간대별 분석

### 6. Report Generator Agent

- 종합 보고서 PDF 생성
- 실행 가능한 인사이트 도출
- 시각적 데이터 표현

## State Management

```python
class State(TypedDict):
    # User Input
    keyword_list: List[str]  # 기술 키워드 목록

    # Research Collector
    collected_papers: Dict[str, List[Dict[str, str]]]  # 키워드별 논문 데이터

    # Tech Summarizer
    summarized_tech: Dict[str, List[str]]  # 키워드별 핵심 기술

    # Trend Predictor
    trend_metrics: Dict[str, Dict[str, float]]  # 기술별 트렌드 메트릭스

    # News Collector
    collected_news: Dict[str, List[Dict[str, str]]]  # 기술별 뉴스 데이터

    # Risk Analyzer
    risk_opportunity_analysis: Dict[str, Dict[str, List[Dict[str, str]]]]  # 리스크/기회 분석

    # Report Generator
    full_report: str  # PDF 보고서 경로
```

## Architecture

![Architecture Diagram](./docs/graph%20diagram.jpg)

## Directory Structure

```
├── agents/           # Agent 모듈
│   ├── base_agent.py
│   ├── research_collector.py
│   ├── tech_summarizer.py
│   ├── trend_predictor.py
│   ├── news_collector.py
│   ├── risk_analyzer.py
│   └── report_generator.py
├── data/            # 수집된 데이터 저장
├── docs/            # 프로젝트 문서
├── outputs/         # 생성된 보고서
├── utils/           # 유틸리티 함수
├── main.py          # 실행 스크립트
├── workflow.py      # Agent 워크플로우
└── requirements.txt # 의존성 패키지
```

## Setup & Installation

1. 환경 설정

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. API 키 설정

```bash
cp .env.example .env
# .env 파일에 필요한 API 키 입력
```

3. 실행

```bash
python main.py
```

## Contributors

- 김선규: 프로젝트 설계 및 구현
