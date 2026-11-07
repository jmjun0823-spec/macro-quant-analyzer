# dcf_valuation.py
import numpy as np
import pandas as pd

def calculate_dcf_value(fcf_projections: list, discount_rate: float, terminal_growth: float) -> float:
    """
    블로그 포스팅의 현금흐름할인(DCF) 공식을 적용하여 기업의 내재가치(V)를 계산합니다.
    Formula: V = sum(FCF_t / (1 + r)^t) + Terminal_Value / (1 + r)^n
    """
    pv_fcf = 0.0
    for t, fcf in enumerate(fcf_projections, start=1):
        pv_fcf += fcf / ((1 + discount_rate) ** t)
    
    last_fcf = fcf_projections[-1]
    terminal_value = (last_fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    pv_terminal_value = terminal_value / ((1 + discount_rate) ** len(fcf_projections))
    
    return pv_fcf + pv_terminal_value

def run_rate_sensitivity_analysis(fcf_projections: list, base_r: float, stressed_r: float, g: float) -> dict:
    """할인율 상승(r ↑)에 따른 기업 내재가치 하락 민감도를 분석합니다."""
    base_val = calculate_dcf_value(fcf_projections, base_r, g)
    stressed_val = calculate_dcf_value(fcf_projections, stressed_r, g)
    impact_pct = ((stressed_val - base_val) / base_val) * 100
    
    return {
        "base_valuation": base_val,
        "stressed_valuation": stressed_val,
        "valuation_change_pct": impact_pct
    }
