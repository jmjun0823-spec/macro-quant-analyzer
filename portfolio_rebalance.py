# portfolio_rebalance.py
import pandas as pd

def calculate_portfolio_performance(price_df: pd.DataFrame, weights: dict) -> pd.DataFrame:
    """포트폴리오 비중 확대(빅테크/반도체) 및 축소(고채무/고배당 레버리지) 리밸런싱 전략 성과 분석."""
    returns = price_df.pct_change().dropna()
    portfolio_daily_ret = sum(returns[col] * weight for col, weight in weights.items() if col in returns.columns)
    
    cum_returns = (1 + portfolio_daily_ret).cumprod() - 1
    return pd.DataFrame({"Daily_Return": portfolio_daily_ret, "Cumulative_Return": cum_returns})
