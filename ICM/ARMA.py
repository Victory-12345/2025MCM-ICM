import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# 假设你的数据已经加载为 DataFrame
data = pd.read_csv('summerOly_medal_counts.csv')

# 将 Year 设置为时间索引
data.set_index('Year', inplace=True)

# 定义一个函数，根据国家和年份进行 ARMA 预测
def arma_forecast_total_by_country(country_name, year, data):
    # 确保年份为整数并且数据按年份排序
    year = int(year)
    data_sorted = data.sort_index()

    # 过滤出指定国家的数据
    country_data = data_sorted[data_sorted['Country'] == country_name]

    # 只选择到指定年份的数据
    country_data_before_year = country_data[country_data.index < year]

    # 如果指定的国家和年份的数据不足，返回一个提示
    if country_data_before_year.empty:
        return f"没有足够的数据来进行预测: {country_name} 在 {year} 年之前没有奖牌数据。"

    # 提取总奖牌数
    total_medals = country_data_before_year['Total']

    # 创建一个新的索引，从 1 开始递增，长度与奖牌数据相同
    new_index = range(1, len(total_medals) + 1)

    # 将奖牌数据的索引替换为新的连续索引
    total_medals.index = new_index

    # 使用线性插值填充缺失的年份
    total_medals_interpolated = total_medals.interpolate(method='linear')

    # 拟合 ARIMA 模型（可以选择适当的 (p, d, q) 参数）
    model = ARIMA(total_medals_interpolated, order=(2, 1, 2))  # 使用 ARIMA 模型，设置 (p, d, q)
    fitted_model = model.fit()

    # 输出模型摘要
    print(f"模型摘要（国家: {country_name}, 年份: {year}）:")
    print(fitted_model.summary())

    # 预测未来 5 年奖牌数
    forecast = fitted_model.get_forecast(steps=5)
    forecast_values = forecast.predicted_mean
    confidence_intervals = forecast.conf_int()

    # 创建预测年份的索引，确保从给定的 'year' 开始
    forecast_years = pd.date_range(start=f'{year + 4}', periods=5, freq='4Y').year

    # 设置预测值和置信区间的索引为预测的年份
    forecast_values.index = forecast_years
    confidence_intervals.index = forecast_years

    # 返回预测值和置信区间
    return forecast_values, confidence_intervals

# 例如，调用函数进行预测（以加拿大和 2024 年为例）
forecast_values, confidence_intervals = arma_forecast_total_by_country('France', 2024, data)

# 打印预测值和置信区间
print("\n预测值:")
print(forecast_values)
print("\n置信区间:")
print(confidence_intervals)
