# config.py
"""
매크로 퀀트 분석 설정 파일
"""

START_DATE = "2025-01-01"
END_DATE = "2026-11-07"

# DCF 할인율 및 영구성장률 변수
BASE_DISCOUNT_RATE = 0.08      # 기본 할인율 (8.0%)
STRESSED_DISCOUNT_RATE = 0.10  # 금리 상방 압력 시 할인율 (10.0%)
TERMINAL_GROWTH_RATE = 0.02   # 영구 성장률 (2.0%)

# 분석 대상 티커 그룹
TICKER_GROUPS = {
    "BIG_TECH": ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN"],
    "SEMICON": ["SOXX", "NVDA", "TSM"],
    "BENCHMARK": ["SPY", "QQQ"],
    "LEVERAGE": ["TQQQ", "SOXL"],
    "VOLATILITY": "^VIX"
}

# 2026년 11월 2주차 타겟 포트폴리오 비중
TARGET_PORTFOLIO_WEIGHTS = {
    "BIG_TECH": 0.40,
    "SEMICON": 0.25,
    "FINANCIAL": 0.15,
    "HIGH_YIELD_LEVERAGE": 0.05,
    "CASH_EQUIVALENT": 0.15
}
