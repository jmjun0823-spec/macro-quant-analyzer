# volatility_drag.py
import numpy as np
import pandas as pd

def simulate_volatility_drag(initial_price: float = 100.0, daily_vol: float = 0.025, days: int = 60, leverage: float = 3.0) -> pd.DataFrame:
    """
    횡보/고변동성 장세에서 2배 및 3배 레버리지 상품의 음의 복리 마모(Volatility Drag) 효과를 시뮬레이션합니다.
    """
    np.random.seed(42)
    daily_returns = np.random.normal(loc=0.0001, scale=daily_vol, size=days)
    
    underlying = [initial_price]
    leveraged = [initial_price]
    
    for r in daily_returns:
        underlying.append(underlying[-1] * (1 + r))
        leveraged.append(leveraged[-1] * (1 + (r * leverage)))
        
    df = pd.DataFrame({
        "Day": range(days + 1),
        "Underlying": underlying,
        f"Leveraged_{leverage}X": leveraged
    })
    
    df["Underlying_Return_%"] = (df["Underlying"] / initial_price - 1) * 100
    df[f"Leveraged_{leverage}X_Return_%"] = (df[f"Leveraged_{leverage}X"] / initial_price - 1) * 100
    
    return df
