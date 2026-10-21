"""
글로벌 파라미터 및 API 키 설정 (동적 날짜 적용)
"""
import os
from datetime import datetime

# ECOS (한국은행), OpenDART, FRED API 키
ECOS_API_KEY = os.getenv("ECOS_API_KEY", "YOUR_ECOS_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY", "YOUR_FRED_API_KEY")

# 기본 분석 시작일 (3년 전 시점부터)
START_DATE = "2023-01-01"

# 실행 당일(오늘) 기준 날짜 자동 설정
END_DATE = datetime.today().strftime("%Y-%m-%d")

# 주요 자산 티커 설정
US_TICKERS = {
    "S&P500": "^GSPC",
    "NASDAQ": "^IXIC",
    "VIX": "^VIX",
    "US10Y": "^TNX",
    "SOXX": "SOXX"
}

KR_TICKERS = {
    "KOSPI": "1001",
    "KOSDAQ": "2001",
    "KOSPI200": "1028"
}
