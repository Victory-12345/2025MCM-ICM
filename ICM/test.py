import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, arma_order_select_ic
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

# Your Gold_rate time series
gold_rate_interpolated = pd.Series(
    {
        1: 0.255814, 2: 0.197917, 3: 0.783505, 4: 0.209091, 5: 0.254902,
        6: 0.264516, 7: 0.357143, 8: 0.200000, 9: 0.170213, 10: 0.275362,
        11: 0.268456, 12: 0.209150, 13: 0.220859, 14: 0.258621, 15: 0.169231,
        16: 0.171717, 17: 0.367257, 18: 0.149378, 19: 0.142308, 20: 0.162362,
        21: 0.123333, 22: 0.119601, 23: 0.119205, 24: 0.158416, 25: 0.150327,
        26: 0.114706, 27: 0.121951,
    }
)

# 1. Check the stationarity of the time series (ADF test)
def check_stationarity(series):
    print("1. Stationarity Test (ADF)")
    result = adfuller(series)
    print("ADF Statistic:", result[0])
    print("p-value:", result[1])
    print("Critical Values:", result[4])
    if result[1] < 0.05:
        print("The series is stationary")
    else:
        print("The series is non-stationary and needs differencing")
    print("-" * 50)

# 2. Plot ACF and PACF
def plot_acf_pacf(series, lags=None):
    if lags is None or lags > len(series) // 2:
        lags = len(series) // 2  # Ensure lags does not exceed 50% of the time series length
    print(f"2. Plot ACF and PACF (lags={lags})")
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plot_acf(series, lags=lags, ax=plt.gca())
    plt.title("ACF Plot")
    plt.subplot(122)
    plot_pacf(series, lags=lags, ax=plt.gca())
    plt.title("PACF Plot")
    plt.tight_layout()
    plt.show()
    print("-" * 50)

# 3. Automatically select the best model parameters
def select_arma_order(series, max_ar=3, max_ma=3):
    print("3. Automatically Select the Best ARMA Model Parameters")
    order_selection = arma_order_select_ic(series, ic='aic', max_ar=max_ar, max_ma=max_ma)
    print("Best model order (p, q):", order_selection['aic_min_order'])
    print("-" * 50)
    return order_selection['aic_min_order']

# 4. Fit the model and analyze residuals
def fit_model_and_residual_analysis(series, order):
    print("4. Fit Model and Analyze Residuals")
    model = ARIMA(series, order=order)
    fitted_model = model.fit()
    print("Model Summary:")
    print(fitted_model.summary())

    # Ljung-Box test to check if residuals are white noise
    ljung_box_result = acorr_ljungbox(fitted_model.resid, lags=[10], return_df=True)
    print("\nLjung-Box Test Result:")
    print(ljung_box_result)

    # Plot ACF of residuals
    print("\nPlot ACF of Residuals...")
    plt.figure(figsize=(6, 4))
    plot_acf(fitted_model.resid, lags=20, ax=plt.gca())
    plt.title("ACF of Residuals")
    plt.tight_layout()
    plt.show()
    print("-" * 50)

# Execute all steps
print("Starting time series analysis...\n")

# 1. Check the stationarity of the time series
check_stationarity(gold_rate_interpolated)

# 2. Plot ACF and PACF
plot_acf_pacf(gold_rate_interpolated)

# 3. Automatically select the best model parameters
best_order = select_arma_order(gold_rate_interpolated)

# 4. Fit the model and analyze residuals
fit_model_and_residual_analysis(gold_rate_interpolated, order=(best_order[0], 0, best_order[1]))

print("Time series analysis completed!")