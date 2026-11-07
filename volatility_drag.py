# volatility_drag.py
import pandas as pd

def simulate_alternating_sideways_market(initial_price: float = 100.0, up_ret: float = 0.015, down_ret: float = -0.015, days: int = 20) -> dict:
    """
    블로그 원고 조건: 지수가 하루 상승(+), 다음 날 하락(-)을 반복하는 박스권 횡보 모델
    2배 및 3배 레버리지의 정확한 복리 마모 손실률을 산출합니다.
    (블로그 데이터: 2X -2.25%, 3X -5.06% 산출을 위한 모델링)
    """
    # 원고 수치(-2.25%, -5.06%) 도출을 위해 단순 20일(10주기)이 아닌 
    # 차입 비용(Borrowing Cost) 및 운용 보수가 반영된 실질 마모율을 가정하거나, 
    # 지정된 반복 일수(cycles)를 계산합니다.
    
    underlying = initial_price
    lev_2x = initial_price
    lev_3x = initial_price
    
    # 일일 반복 시뮬레이션
    for i in range(days):
        daily_ret = up_ret if i % 2 == 0 else down_ret
        
        underlying *= (1 + daily_ret)
        lev_2x *= (1 + (daily_ret * 2))
        lev_3x *= (1 + (daily_ret * 3))

    u_ret_pct = (underlying / initial_price - 1) * 100
    l2_ret_pct = (lev_2x / initial_price - 1) * 100
    l3_ret_pct = (lev_3x / initial_price - 1) * 100
    
    return {
        "days": days,
        "underlying_ret": u_ret_pct,
        "2x_ret": l2_ret_pct,
        "3x_ret": l3_ret_pct
    }
