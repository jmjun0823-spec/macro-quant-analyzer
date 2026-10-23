import os
from datetime import datetime, timedelta

# ECOS (한국은행), OpenDART, FRED API 키
ECOS_API_KEY = os.getenv("ECOS_API_KEY", "YOUR_ECOS_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY", "YOUR_FRED_API_KEY")

# 기본 분석 시작일 (3년 전 시뮬레이션)
END_DATE = datetime.today().strftime('%Y-%m-%d')
START_DATE = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

# 주요 자산 티커 설정
US_TICKERS = {
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
    "SOXX": "SOXX",
    "S&P500": "^GSPC",
    "NASDAQ": "^IXIC",
    "US10Y": "^TNX",
    "VIX": "^VIX"
}

KR_TICKERS = {
    "KOSPI": "1001",
    "KOSDAQ": "2001",
    "KOSPI200": "1028"
}
