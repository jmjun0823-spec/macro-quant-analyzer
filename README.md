# macro-quant-analyzer

**저장소 설명:**
2026년 11월 2주차 주간 증시 전망 포스팅의 핵심 매크로 및 퀀트 주장을 실증 데이터로 입증하기 위한 분석 프로젝트입니다. 통화정책 전환기(Pivot)의 DCF 할인율 민감도 평가, 변동성 장세에서의 레버리지/고배당 ETF 음의 복리 마모(Volatility Drag) 시뮬레이션, 수급 불균형 및 리밸런싱 전략을 코드 기반으로 검증합니다.

## 주요 기능
1. **DCF Valuation & Sensitivity Analysis (`dcf_valuation.py`)**: 금리 상방 압력 및 할인율($r$) 변화에 따른 기업 내재가치 변동 정량 분석.
2. **Volatility Drag Simulator (`volatility_drag.py`)**: 고변동성/횡보장 조건에서 2배·3배 레버리지 상품의 기하수익률 마모 및 손실폭 계산.
3. **Portfolio Rebalancing Engine (`portfolio_rebalance.py`)**: 빅테크·반도체 비중 확대 및 레버리지/고부채주 비중 축소 전략 백테스팅.
4. **Data Loader (`data_loader.py`)**: Market Data(지수, VIX, FCF, 국채금리 등) 자동 수집 파이프라인.

## 실행 방법
```bash
pip install -r requirements.txt
python main.py
