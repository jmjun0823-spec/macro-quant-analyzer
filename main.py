# main.py
import pandas as pd
from config import BASE_DISCOUNT_RATE, STRESSED_DISCOUNT_RATE, TERMINAL_GROWTH_RATE
from dcf_valuation import run_rate_sensitivity_analysis
from volatility_drag import simulate_volatility_drag

def main():
    print("=" * 65)
    print(" [혜안 퀀트 분석 랩] 2026년 11월 2주차 주간 증시 포스팅 검증 프로젝트")
    print("=" * 65)
    
    # 1. DCF 할인율 민감도 검증
    sample_fcf = [1200, 1400, 1650, 1900, 2200]  # 단위: 억 달러
    dcf_res = run_rate_sensitivity_analysis(sample_fcf, BASE_DISCOUNT_RATE, STRESSED_DISCOUNT_RATE, TERMINAL_GROWTH_RATE)
    
    print("\n[1] 매크로 금리 변수(r) 및 밸류에이션 변동 입증")
    print(f" - 기준 할인율 ({BASE_DISCOUNT_RATE*100:.1f}%): ${dcf_res['base_valuation']:,.2f}")
    print(f" - 상방 할인율 ({STRESSED_DISCOUNT_RATE*100:.1f}%): ${dcf_res['stressed_valuation']:,.2f}")
    print(f" - 기업 내재가치 하락 민감도: {dcf_res['valuation_change_pct']:.2f}%\n")
    
    # 2. Volatility Drag (음의 복리 마모) 입증
    drag_df = simulate_volatility_drag(initial_price=100.0, daily_vol=0.025, days=60, leverage=3.0)
    u_ret = drag_df["Underlying_Return_%"].iloc[-1]
    l_ret = drag_df["Leveraged_3.0X_Return_%"].iloc[-1]
    
    print("[2] 변동성 장세 레버리지 음의 복리 마모(Volatility Drag) 입증")
    print(f" - 60일 기초자산 누적 수익률: {u_ret:.2f}%")
    print(f" - 3배 레버리지 최종 수익률: {l_ret:.2f}%")
    print(f" - 음의 복리 마모 손실차: {l_ret - (u_ret * 3):.2f}%p\n")
    print("=" * 65)

if __name__ == "__main__":
    main()
