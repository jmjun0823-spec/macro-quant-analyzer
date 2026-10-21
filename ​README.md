# Macro-Quant Analyzer (혜안 퀀트 분석 모듈)

경제 블로그 **혜안**의 매크로 경제 지표 및 증시 데이터 분석 자동화 파이프라인입니다.

## 📂 프로젝트 구조
```text
macro-quant-analyzer/
├── README.md                 # 프로젝트 개요 및 실행 방법
├── requirements.txt          # 파이썬 라이브러리 의존성
├── config.py                 # 동적 날짜(오늘) 및 API/티커 글로벌 설정
├── src/
│   ├── __init__.py
│   ├── data_collector.py     # 파이썬 데이터 수집 (PyKRX, yfinance, BOK ECOS)
│   ├── stat_test.py          # 변동성 드래그 시뮬레이션 & DSR 소비 마모 검정
│   └── quant_strategy.py     # 밸류에이션 스플릿 상관분석 & 바벨 포트폴리오
└── scripts/
    └── macro_econometrics.R  # R 시계열 VAR 및 공적분(Cointegration) 검정
