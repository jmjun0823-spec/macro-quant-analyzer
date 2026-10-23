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
    
    # 데이터 수집 및 저장
    market_data = collector.fetch_market_data()
    market_data.to_csv('market_data.csv')
    print("[INFO] market_data.csv 파일 저장 완료!")
    
    # --- 퀀트 전략 및 K자형 격차 분석 연동 ---
    try:
        from quant_strategy import calculate_rolling_beta, optimize_barbell_portfolio, calculate_valuation_split_correlation
        
        print("\n" + "="*50)
        print(" [INFO] K자형 경제 격차 및 퀀트 전략 분석 실행")
        print("="*50)
        
        # 1. 롤링 베타 분석
        if 'KOSPI' in market_data.columns and 'S&P500' in market_data.columns:
            clean_data = market_data[['KOSPI', 'S&P500']].dropna()
            rolling_beta = calculate_rolling_beta(clean_data['KOSPI'], clean_data['S&P500'], window=5)
            print("\n[1] Rolling Beta (S&P500 대비 KOSPI):\n", rolling_beta.tail(3))
            
        # 2. 바벨 포트폴리오 최적화 (주식 vs 채권)
        if 'S&P500' in market_data.columns and 'US10Y' in market_data.columns:
            barbell_returns = market_data[['S&P500', 'US10Y']].pct_change().dropna()
            if not barbell_returns.empty:
                barbell_result = optimize_barbell_portfolio(barbell_returns)
                print("\n[2] 바벨 포트폴리오 최적화 결과:")
                for k, v in barbell_result.items():
                    print(f"  - {k}: {v}")

        # 3. 수출 vs 내수 밸류에이션/수익률 격차 분석 (추가 확장)
        # 만약 데이터프레임에 수출/내수 지표가 있다면 연동하여 상관관계 및 격차 분석 수행
        print("\n[3] 수출 vs 내수 양극화 분석 모듈 연동 준비 완료")
        
        print("\n" + "="*50)
        print(" [INFO] 모든 분석 완료!")
        print("="*50)
        
    except Exception as e:
        print(f"[WARN] 분석 실행 중 예외 발생: {e}")
