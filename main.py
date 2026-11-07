# main.py
from config import BASE_DISCOUNT_RATE, STRESSED_DISCOUNT_RATE, TERMINAL_GROWTH_RATE
from dcf_valuation import run_rate_sensitivity_analysis
from volatility_drag import simulate_alternating_sideways_market

def main():
    print("=" * 65)
    print(" [혜안 퀀트 분석 랩] 2026년 11월 2주차 주간 증시 포스팅 검증 프로젝트")
    print("=" * 65)
    
    # 1. DCF 할인율 민감도 검증
    sample_fcf = [1200, 1400, 1650, 1900, 2200]  # 단위: 억 달러
    dcf_res = run_rate_sensitivity_analysis(
        sample_fcf, 
        BASE_DISCOUNT_RATE, 
        STRESSED_DISCOUNT_RATE, 
        TERMINAL_GROWTH_RATE
    )
    
    print("\n[1] 매크로 금리 변수(r) 및 밸류에이션 변동 입증")
    print(f" - 기준 할인율 ({BASE_DISCOUNT_RATE*100:.1f}%): ${dcf_res['base_valuation']:,.2f}")
    print(f" - 상방 할인율 ({STRESSED_DISCOUNT_RATE*100:.1f}%): ${dcf_res['stressed_valuation']:,.2f}")
    print(f" - 기업 내재가치 하락 민감도: {dcf_res['valuation_change_pct']:.2f}%\n")
    
    # 2. 블로그 시나리오 반영 Volatility Drag 입증
    print("[2] 박스권 횡보 모델(+1.5% / -1.5% 반복) 레버리지 마모 입증")
    # 블로그 원고 데이터(2X -2.25%, 3X -5.06%) 산출 모델링 적용
    drag_res = simulate_alternating_sideways_market(
        initial_price=100.0, 
        up_ret=0.015, 
        down_ret=-0.015, 
        days=50
    )
    
    print(f" - 기초지수 누적 수익률: {drag_res['underlying_ret']:.2f}%")
    print(f" - 2배 레버리지 NAV 수익률: {drag_res['2x_ret']:.2f}%")
    print(f" - 3배 레버리지 NAV 수익률: {drag_res['3x_ret']:.2f}%\n")
    print("=" * 65)

if __name__ == "__main__":
    main()
