"""
통계 검정 모듈:
1. 레버리지 ETF의 음의 복리 마모(Volatility Drag) 몬테카를로 가설검정
2. 가계 DSR 상환액 누적과 실질 소비 지출 간 한계소비성향 다중회귀분석
"""
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from typing import Dict, Any


def test_volatility_drag_hypothesis(
    initial_nav: float = 10000.0,
    daily_vol: float = 0.02,
    num_days: int = 20,
    num_simulations: int = 10000
) -> Dict[str, Any]:
    """
    귀무가설(H0): 횡보장에서 지수가 회복되면 2X/3X 레버리지 NAV는 보존된다.
    대립가설(H1): 기하평균 마모 메커니즘에 의해 레버리지 NAV는 통계적으로 유의하게 감소한다.
    """
    np.random.seed(42)
    base_returns = np.tile([daily_vol, -daily_vol], num_days // 2)
    
    nav_1x = initial_nav * np.cumprod(1 + base_returns)
    nav_2x = initial_nav * np.cumprod(1 + 2 * base_returns)
    nav_3x = initial_nav * np.cumprod(1 + 3 * base_returns)
    
    final_2x_returns = []
    for _ in range(num_simulations):
        rand_shocks = np.random.choice([daily_vol, -daily_vol], size=num_days)
        nav_sim = initial_nav * np.cumprod(1 + 2 * rand_shocks)
        final_2x_returns.append(nav_sim[-1])
        
    t_stat, p_value = stats.ttest_1samp(final_2x_returns, initial_nav)
    
    return {
        "final_nav_1x": nav_1x[-1],
        "final_nav_2x": nav_2x[-1],
        "final_nav_3x": nav_3x[-1],
        "t_statistic": t_stat,
        "p_value": p_value,
        "h0_rejected": p_value < 0.01
    }


def reg_dsr_consumption_erosion(
    dsr_series: pd.Series,
    cpi_series: pd.Series,
    consumption_series: pd.Series
) -> sm.regression.linear_model.RegressionResultsWrapper:
    """
    DSR(원리금상환비율) 및 CPI 누적 충격이 실질 소비 지출(Consumption)에 미치는 OLS 회귀분석
    """
    df = pd.concat([consumption_series, dsr_series, cpi_series], axis=1).dropna()
    df.columns = ['Consumption', 'DSR', 'CPI']
    
    X = sm.add_constant(df[['DSR', 'CPI']])
    y = df['Consumption']
    
    return sm.OLS(y, X).fit()


if __name__ == "__main__":
    result = test_volatility_drag_hypothesis()
    print("=== Volatility Drag Hypothesis Test ===")
    print(f"2X ETF Final NAV (after 20 days): {result['final_nav_2x']:.2f}")
    print(f"p-value: {result['p_value']:.6e} | H0 Rejected: {result['h0_rejected']}")
