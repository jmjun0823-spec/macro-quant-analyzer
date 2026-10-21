# ==============================================================================
# R 계량경제 분석: 수출 성장률과 민간 소비 간 공적분(Cointegration) 및 VAR 분석
# ==============================================================================

suppressMessages({
  library(tidyverse)
  library(tseries)
  library(vars)
  library(urca)
})

# 1. 데이터 수집 및 시계열 객체 생성
macro_data <- read.csv("../data/macro_series.csv")
macro_ts <- ts(macro_data[, c("export_growth", "private_consumption", "interest_rate")], 
               start = c(2023, 1), frequency = 12)

# 2. 단위근 검정 (ADF Test)
cat("\n--- [1] ADF Unit Root Test ---\n")
print(adf.test(macro_ts[, "export_growth"]))
print(adf.test(macro_ts[, "private_consumption"]))

# 3. 요한센 공적분 검정 (Johansen Cointegration Test)
cat("\n--- [2] Johansen Cointegration Test ---\n")
johansen_res <- ca.jo(macro_ts, type = "trace", ecdet = "const", K = 2)
summary(johansen_res)

# 4. VAR 모형 적합
cat("\n--- [3] VAR Model Fitting ---\n")
var_lag <- VARselect(macro_ts, lag.max = 4, type = "const")
var_fit <- VAR(macro_ts, p = var_lag$selection["AIC(n)"], type = "const")
summary(var_fit)

# 5. 충격반응함수 (IRF)
irf_res <- irf(var_fit, impulse = "interest_rate", response = "private_consumption", 
               n.ahead = 12, boot = TRUE)
plot(irf_res, main = "IRF: Interest Rate Spike -> Private Consumption")
