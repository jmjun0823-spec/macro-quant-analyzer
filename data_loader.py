# data_loader.py
import yfinance as yf
import pandas as pd
from config import START_DATE, END_DATE, TICKER_GROUPS

def fetch_market_data(tickers: list, start_date: str = START_DATE, end_date: str = END_DATE) -> pd.DataFrame:
    """yfinance를 활용하여 분석 대상 티커의 수정 주가(Adjusted Close)를 수집합니다."""
    data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
    return data

def fetch_macro_indicators() -> pd.DataFrame:
    """VIX 변동성 지수 및 주요 벤치마크 지수 데이터를 수집합니다."""
    macro_tickers = [TICKER_GROUPS["VOLATILITY"]] + TICKER_GROUPS["BENCHMARK"]
    return fetch_market_data(macro_tickers)
