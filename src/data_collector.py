from pykrx import stock
import requests
from typing import Dict, Tuple
import pandas as pd
from config import START_DATE, END_DATE, US_TICKERS, ECOS_API_KEY

class MacroDataCollector:
    def __init__(self, start_date: str = START_DATE, end_date: str = END_DATE):
        self.start_date = start_date
        self.end_date = end_date

    def fetch_us_market_data(self, tickers: Dict[str, str] = US_TICKERS) -> pd.DataFrame:
        """yfinance를 활용한 미국 주요 지수 및 10년물 국채 금리, VIX 수집"""
        print(f"[INFO] 미국 증시 데이터 수집 중... ({self.start_date} ~ {self.end_date})")
        df = yf.download(list(tickers.values()), start=self.start_date, end=self.end_date)
        if 'Adj Close' in df.columns:
            data = df['Adj Close']
        else:
            data = df['Close']
        data.rename(columns={v: k for k, v in tickers.items()}, inplace=True)
        return data

    def fetch_kr_market_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """PyKRX를 활용한 국내 지수 및 투자자(개인/기관/외국인) 수급 데이터 수집"""
        print(f"[INFO] 한국 증시 데이터 수집 중... ({self.start_date} ~ {self.end_date})")
        start = self.start_date.replace("-", "")
        end = self.end_date.replace("-", "")

        # KOSPI 지수 데이터
        kospi_df = stock.get_index_ohlcv_by_date(start, end, "1001")

        # 투자자별 순매수 데이터
        investor_df = stock.get_index_investor_net_purchases_of_equities_by_date(start, end, "1001")

        return kospi_df, investor_df

    def fetch_ecos_indicator(self, stat_code: str, item_code: str, api_key: str = ECOS_API_KEY) -> pd.DataFrame:
        """한국은행 ECOS API를 통한 가계 DSR, 실질임금, 내수소비 지표 수집"""
        start_m = self.start_date[:7].replace("-", "")
        end_m = self.end_date[:7].replace("-", "")
        url = f"http://ecos.bok.or.kr/api/StatisticSearch/{api_key}/json/kr/1/1000/{stat_code}/M/{start_m}/{end_m}/{item_code}/"

        try:
            response = requests.get(url).json()
            rows = response['StatisticSearch']['row']
            df = pd.DataFrame(rows)[['TIME', 'DATA_VALUE']]
            df.columns = ['date', 'value']
            df['value'] = pd.to_numeric(df['value'])
            df['date'] = pd.to_datetime(df['date'], format='%Y%m')
            return df.set_index('date')
        except Exception as e:
            print(f"[WARN] ECOS API 수집 실패: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    collector = MacroDataCollector()
    
    # 1. 미국 데이터 확인
    us_data = collector.fetch_us_market_data()
    print("--- 미국 시장 데이터 ---")
    print(us_data.tail())
    
    # 2. 한국 코스피 및 수급 데이터 확인
    kospi_df, investor_df = collector.fetch_kr_market_data()
    print("--- 코스피 지수 데이터 ---")
    print(kospi_df.tail())
    print("--- 투자자별 순매수 데이터 ---")
    print(investor_df.tail())
