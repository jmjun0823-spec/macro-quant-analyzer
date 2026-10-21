"""
퀀트 전략 모듈:
1. 수출 대형주 vs 내수주 간 밸류에이션 스플릿 (Valuation Split) 상관관계 분석
2. Beta 기반 헤지 계수 산출 및 바벨 포트폴리오(Barbell Portfolio) 최적화
"""
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
from typing import Dict, Any


def calculate_valuation_split_correlation(
    export_pbr: pd.Series,
    domestic_pbr: pd.Series
) -> Dict[str, float]:
    """수출 업종 PBR과 내수 업종 PBR 간 상관계수 검정"""
    df = pd.concat([export_pbr, domestic_pbr], axis=1).dropna()
    df.columns = ['Export', 'Domestic']
    
    p_corr, p_pval = pearsonr(df['Export'], df['Domestic'])
    s_corr, s_pval = spearmanr(df['Export'], df['Domestic'])
    
    return {
        "pearson_corr": p_corr,
        "pearson_pvalue": p_pval,
        "spearman_corr": s_corr,
        "spearman_pvalue": s_pval
    }


def optimize_barbell_portfolio(
    returns_df: pd.DataFrame,
    export_weight: float = 0.60,
    defensive_weight: float = 0.40
) -> Dict[str, Any]:
    """수출주(60%) + 고배당/채권 방어주(40%) 바벨 포트폴리오 샤프 지수 계산"""
    weights = np.array([export_weight, defensive_weight])
    cov_matrix = returns_df.cov() * 252
    
    port_return = np.sum(returns_df.mean() * weights) * 252
    port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe = port_return / port_vol if port_vol > 0 else 0
    
    return {
        "expected_annual_return": port_return,
        "annual_volatility": port_vol,
        "sharpe_ratio": sharpe
    }


def calculate_rolling_beta(asset_returns: pd.Series, market_returns: pd.Series, window: int = 60) -> pd.Series:
    """KOSPI 대비 특정 섹터/종목의 60일 롤링 Beta 산출"""
    df = pd.concat([asset_returns, market_returns], axis=1).dropna()
    df.columns = ['asset', 'market']
    
    cov = df['asset'].rolling(window=window).cov(df['market'])
    var = df['market'].rolling(window=window).var()
    return cov / var
