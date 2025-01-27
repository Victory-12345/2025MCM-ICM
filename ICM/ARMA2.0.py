import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# 加载数据
data = pd.read_csv('summerOly_medal_counts.csv')

# 按年份统计金、银、铜牌总数
medal_totals = data.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum()

# 定义一个函数，根据国家和年份进行 ARMA 预测
def arma_forecast_by_country(country_name, year, data):
    # 确保年份为整数并且数据按年份排序
    year = int(year)
    data_sorted = data.sort_values('Year')

    # 过滤出指定国家的数据
    country_data = data_sorted[data_sorted['Country'] == country_name]

    # 合并每年的奖牌总数到国家数据
    country_data = country_data.merge(medal_totals, on='Year', suffixes=('', '_total'))

    # 计算得奖率
    for medal in ['Gold', 'Silver', 'Bronze']:
        country_data[f'{medal}_rate'] = country_data[medal] / country_data[f'{medal}_total']

    # 筛选出指定年份之前的数据
    country_data_before_year = country_data[country_data['Year'] < year]

    # 如果没有足够数据，返回提示
    if country_data_before_year.empty:
        return f"没有足够的数据来进行预测: {country_name} 在 {year} 年之前没有奖牌数据。"

    forecast_results = {}

    for medal in ['Gold', 'Silver', 'Bronze']:
        # 提取得奖率序列
        medal_rate = country_data_before_year.set_index('Year')[f'{medal}_rate']

        # 创建一个新的索引，从 1 开始递增
        new_index = range(1, len(medal_rate) + 1)
        medal_rate.index = new_index

        # 使用线性插值填充缺失值
        medal_rate_interpolated = medal_rate.interpolate(method='linear')

        # 拟合 ARIMA 模型（设置 (p, d, q) 参数）
        model = ARIMA(medal_rate_interpolated, order=(2, 1, 2))
        fitted_model = model.fit()

        # 预测未来 5 届奥运会的得奖率
        forecast = fitted_model.get_forecast(steps=5)
        forecast_rates = forecast.predicted_mean

        # 获取上一届奥运会的奖牌总数
        last_olympics_totals = medal_totals.loc[medal_totals.index < year].iloc[-1]

        # 根据预测得奖率和上一届奖牌总数计算预测奖牌数
        forecast_medal = forecast_rates * last_olympics_totals[medal]

        # 创建预测年份索引
        forecast_years = pd.date_range(start=f'{year + 4}', periods=5, freq='4Y').year
        forecast_medal.index = forecast_years

        # 包含预测数的数据表
        forecast_results[medal] = pd.DataFrame({
            f'Forecasted {medal}': forecast_medal
        })

    # 合并金、银、铜牌预测结果并计算总奖牌预测
    combined_forecast = pd.concat(forecast_results, axis=1)
    combined_forecast['Total Forecasted Medals'] = combined_forecast['Gold']['Forecasted Gold'] + combined_forecast['Silver']['Forecasted Silver'] + combined_forecast['Bronze']['Forecasted Bronze']

    return combined_forecast

# 示例调用函数进行预测
forecast_result = arma_forecast_by_country('France', 2024, data)

# 打印预测结果
print("\n预测奖牌数量：")
print(forecast_result)