# TITLE

본 프로젝트는 미래 기술 트렌드 분석 에이전트를 설계하고 구현한 실습 프로젝트입니다.

## Overview

- Objective : AI를 포함한 미래 기술 트렌드를 데이터 기반으로 분석하고, 향후 5년 내 주목해야 할 기술을 도출하여 보고서로 제시합니다.
- Methods : 논문/뉴스 수집 자동화, 요약 및 트렌드 예측, 보고서 작성
- Tools : LangGraph, Google Scholar API, Google Trends API, Google News API

## Features

- 최근 3년 간 주요 기술 키워드 기반 논문/뉴스 자동 수집
- LLM 기반 핵심 기술 요약 및 트렌드 예측
- 시장성, 기술성, 리스크 기반 통합 보고서 자동 생성

## Tech Stack

| Category  | Details                      |
| --------- | ---------------------------- |
| Framework | LangGraph, LangChain, Python |
| LLM       | GPT-4o-mini via OpenAI API   |
| Retrieval | Chroma                       |

## Agents

- Research Collector Agent: 키워드 별 최신 연구 수집
  - 사용자가 설정 키워드를 바탕으로 Google Scholar API를 통해 최근 3년 간 연구 논문 수집
- Tech Summarizer Agent: 핵심 기술 요약
  - 키워드 별로 수집한 논문들의 핵심 기술 요약
- Trend Predictor Agent: 기술 트렌드 예측
  - Google Scholar API를 통해 논문 수 증가율 파악
  - Google Scholar API를 통해 인용 수 증가율 파악
  - Google Trends API를 통해 검색량 기반으로 트렌드 파악
- News Collector Agent: 핵심 기술 별 최신 뉴스 수집
  - Google News API를 통해 최근 3년 간 핵심 기술 관련 뉴스 수집
- Risk Analyzer Agent: 기회/리스크 분석
  - 핵심 기술 별로 수집한 뉴스를 기반으로 기회 및 리스크 분석
- Report Gen Agent: 보고서 생성
  - 트렌드 분석 결과를 바탕으로 보고서 작성

## State

- raw_data: 수집된 논문, 뉴스 등 원본 텍스트 및 메타데이터
- summarized_data: 기술별 핵심 요약 정보
- trend_insight: 키워드별 트렌드 분석 정보 (논문 수/인용수 증가율, 검색량 변화 등)
- risk_opportunity: 키워드별 기회 및 리스크 요인
- final_report: 전체 결과를 종합한 트렌드 보고서

## Architecture

![diagram](./docs/graph%20diagram.jpg)

## Directory Structure

```
├── data/       # Agent가 수집한 자료
├── agents/     # Agent 모듈
├── prompts/    # 프롬프트 템플릿
├── outputs/    # 보고서 저장
├── main.py     # 실행 스크립트
└── readme.md
```

## Contributors

- 김선규 : overall of project
