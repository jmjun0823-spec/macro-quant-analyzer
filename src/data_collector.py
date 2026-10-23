import yfinance as yf
import requests
from typing import Dict
import pandas as pd
from config import START_DATE, END_DATE, US_TICKERS, ECOS_API_KEY

class MacroDataCollector:
    def __init__(self, start_date: str = START_DATE, end_date: str = END_DATE):
        self.start_date = start_date
        self.end_date = end_date

    def fetch_market_data(self, tickers: Dict[str, str] = US_TICKERS) -> pd.DataFrame:
        """yfinance를 활용해 코스피, 코스닥 및 글로벌 주요 지수 최근 1달 데이터 수집"""
        print(f"[INFO] 국내외 증시 데이터 수집 중... ({self.start_date} ~ {self.end_date})")
        df = yf.download(list(tickers.values()), start=self.start_date, end=self.end_date)
        
        if 'Adj Close' in df.columns:
            data = df['Adj Close']
        else:
            data = df['Close']
            
        # 티커 이름을 알아보기 쉽게 컬럼명으로 매핑
        data.rename(columns={v: k for k, v in tickers.items()}, inplace=True)
        return data

    def fetch_ecos_indicator(self, stat_code: str, item_code: str, api_key: str = ECOS_API_KEY) -> pd.DataFrame:
        """한국은행 ECOS API 거시경제 지표 수집"""
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
    
    # 최근 1달간의 국내외 증시 데이터 수집 및 출력
    market_data = collector.fetch_market_data()
    print("--- 국내외 주요 증시 데이터 (최근 1달) ---")
    print(market_data.tail(15))
