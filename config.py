import pandas as pd
import numpy as np
from data_collector import MacroDataCollector  # 기존 클래스 임포트

if __name__ == "__main__":
    collector = MacroDataCollector()
    
    # 판다스 출력 옵션 설정 (로그 가독성 향상)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)
    
    # 1. 최근 1달간의 국내외 증시 데이터 수집
    market_data = collector.fetch_market_data()
    print("--- 국내외 주요 증시 데이터 (최근 1달 전체) ---")
    print(market_data)
    
    # 2. CSV 파일 저장
    market_data.to_csv('market_data.csv')
    print("[INFO] market_data.csv 파일 저장 완료!")
    
    # 3. 퀀트 전략 분석 로직 연동 실행
    try:
        from quant_strategy import calculate_rolling_beta, optimize_barbell_portfolio
        
        print("\n" + "="*50)
        print(" [INFO] 퀀트 전략 분석 실행 시작")
        print("="*50)
        
        # 3-1. 롤링 베타 분석 (S&P500 대비 KOSPI, 5일 윈도우)
        print("\n[1] Rolling Beta (S&P500 대비 KOSPI)")
        if 'KOSPI' in market_data.columns and 'S&P500' in market_data.columns:
            clean_data = market_data[['KOSPI', 'S&P500']].dropna()
            rolling_beta = calculate_rolling_beta(clean_data['KOSPI'], clean_data['S&P500'], window=5)
            print(rolling_beta.tail(5))
            
        # 3-2. 바벨 포트폴리오 최적화 분석 (S&P500 vs US10Y 2개 자산)
        print("\n[2] 바벨 포트폴리오 최적화 결과 (S&P500 vs US10Y)")
        if 'S&P500' in market_data.columns and 'US10Y' in market_data.columns:
            barbell_returns = market_data[['S&P500', 'US10Y']].pct_change().dropna()
            if not barbell_returns.empty:
                barbell_result = optimize_barbell_portfolio(barbell_returns)
                for key, val in barbell_result.items():
                    print(f"  - {key}: {val}")
                
        print("\n" + "="*50)
        print(" [INFO] 모든 퀀트 분석 완료!")
        print("="*50)
        
    except Exception as e:
        print(f"[WARN] 퀀트 분석 실행 중 예외 발생: {e}")
