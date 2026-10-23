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
    
    # 판다스 출력 옵션 설정
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)
    
    # 최근 1달간의 국내외 증시 데이터 수집 및 출력
    market_data = collector.fetch_market_data()
    print("--- 국내외 주요 증시 데이터 (최근 1달 전체 질) ---")
    print(market_data)
    
    # CSV 파일 저장
    market_data.to_csv('market_data.csv')
    print("[INFO] market_data.csv 파일 저장 완료!")
    
    # --- [추가] quant_strategy.py 분석 로직 연동 실행 ---
    try:
        from quant_strategy import calculate_rolling_beta
        print("\n--- 퀀트 전략 분석 결과 (Rolling Beta 예시) ---")
        # 예시로 S&P500(^GSPC) 대비 코스피(KOSPI)의 5일 롤링 베타 계산
        if 'KOSPI' in market_data.columns and 'S&P500' in market_data.columns:
            # NaN 제거 후 계산
            clean_data = market_data[['KOSPI', 'S&P500']].dropna()
            rolling_beta = calculate_rolling_beta(clean_data['KOSPI'], clean_data['S&P500'], window=5)
            print(rolling_beta.tail(5))
    except Exception as e:
        print(f"[WARN] 퀀트 분석 실행 중 예외 발생: {e}")
