"""
글로벌 파라미터 및 API 키 설정 (동적 날짜 적용)
"""
import os
from datetime import datetime, timedelta

# ECOS (한국은행), OpenDART, FRED API 키
ECOS_API_KEY = os.getenv("ECOS_API_KEY", "YOUR_ECOS_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY", "YOUR_FRED_API_KEY")

# 기본 분석 시작일 (3년 전 시점부터)
# 오늘 날짜와 정확히 30일(1달) 전 날짜를 동적으로 계산
END_DATE = datetime.today().strftime('%Y-%m-%d')
START_DATE = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

# 실행 당일(오늘) 기준 날짜 자동 설정
END_DATE = datetime.today().strftime("%Y-%m-%d")

# 주요 자산 티커 설정
# US_TICKERS나 별도의 딕셔너리에 코스피 지수 추가 예시
US_TICKERS = {
    "KOSPI": "^KS11",     # 코스피 지수 추가
    "KOSDAQ": "^KQ11",    # 코스닥 지수 추가
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
