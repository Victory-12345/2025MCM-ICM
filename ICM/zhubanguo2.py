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

    # 过滤出目标年份之前的数据
    data_sorted = data_sorted[data_sorted['Year'] < year]

    # 过滤出指定国家的数据
    country_data = data_sorted[data_sorted['Country'] == country_name]

    # 合并每年的奖牌总数到国家数据
    country_data = country_data.merge(medal_totals, on='Year', suffixes=('', '_total'))

    # 计算得奖率
    country_data['Gold_rate'] = country_data['Gold'] / country_data['Gold_total']
    country_data['Silver_rate'] = country_data['Silver'] / country_data['Silver_total']
    country_data['Bronze_rate'] = country_data['Bronze'] / country_data['Bronze_total']

    # 如果没有足够数据，返回提示
    if country_data.empty or len(country_data) < 10:  # 限制最少数据点数
        return None

    # 提取得奖率序列
    gold_rate = country_data.set_index('Year')['Gold_rate']

    # 创建一个新的索引，从 1 开始递增
    new_index = range(1, len(gold_rate) + 1)
    gold_rate.index = new_index

    # 使用线性插值填充缺失值
    gold_rate_interpolated = gold_rate.interpolate(method='linear')

    # 拟合 ARIMA 模型（设置 (p, d, q) 参数）
    try:
        model = ARIMA(gold_rate_interpolated, order=(2, 1, 2))
        fitted_model = model.fit()
    except Exception as e:
        print(f"ARIMA 模型拟合失败（国家: {country_name}, 年份: {year}）: {e}")
        return None

    # 预测未来 1 届奥运会的得奖率
    forecast = fitted_model.get_forecast(steps=1)
    forecast_rate = forecast.predicted_mean.iloc[0]

    # 获取上一届奥运会的奖牌总数
    last_olympics_totals = medal_totals.loc[medal_totals.index < year].iloc[-1]

    # 根据预测得奖率和上一届奖牌总数计算预测奖牌数
    forecast_gold = forecast_rate * last_olympics_totals['Gold']

    return forecast_gold

# 对每一年（1988-2024）进行预测并计算残差
country_name = 'Spain'
results = []

for year in range(1984, 2025, 4):  # 从1988到2024，每4年一次
    forecast_gold = arma_forecast_by_country(country_name, year, data)

    # 如果没有足够数据，跳过该年份
    if forecast_gold is None:
        continue

    # 获取实际金牌数
    actual_gold = data[(data['Country'] == country_name) & (data['Year'] == year)]['Gold'].sum()

    # 计算残差
    residual = actual_gold - forecast_gold

    # 保存结果
    results.append({'Year': year, 'Forecast_Gold': forecast_gold, 'Actual_Gold': actual_gold, 'Residual': residual})

# 转换为 DataFrame 并输出
results_df = pd.DataFrame(results)

# 打印预测结果和残差
print("\n预测结果与残差:")
print(results_df)
# import pandas as pd
# from statsmodels.tsa.arima.model import ARIMA

# # 加载数据
# data = pd.read_csv('summerOly_medal_counts.csv')

# # 定义一个函数，根据国家和年份进行 ARMA 预测
# def arma_forecast_by_country(country_name, year, data):
#     # 确保年份为整数并且数据按年份排序
#     year = int(year)
#     data_sorted = data.sort_values('Year')

#     # 过滤出目标年份之前的数据
#     data_sorted = data_sorted[data_sorted['Year'] < year]

#     # 过滤出指定国家的数据
#     country_data = data_sorted[data_sorted['Country'] == country_name]

#     # 如果没有足够数据，返回提示
#     if country_data.empty or len(country_data) < 10:  # 限制最少数据点数
#         return None

#     # 提取总奖牌数序列
#     total_medals = country_data.set_index('Year')['Total']

#     # 创建一个新的索引，从 1 开始递增
#     new_index = range(1, len(total_medals) + 1)
#     total_medals.index = new_index

#     # 使用线性插值填充缺失值
#     total_medals_interpolated = total_medals.interpolate(method='linear')

#     # 拟合 ARIMA 模型（设置 (p, d, q) 参数）
#     try:
#         model = ARIMA(total_medals_interpolated, order=(2, 1, 2))
#         fitted_model = model.fit()
#     except Exception as e:
#         print(f"ARIMA 模型拟合失败（国家: {country_name}, 年份: {year}）: {e}")
#         return None

#     # 预测未来 1 届奥运会的奖牌总数
#     forecast = fitted_model.get_forecast(steps=1)
#     forecast_total_medals = forecast.predicted_mean.iloc[0]

#     return forecast_total_medals

# # 对每一年（1988-2024）进行预测并计算残差
# country_name = 'Spain'
# results = []

# for year in range(1988, 2025, 4):  # 从1988到2024，每4年一次
#     forecast_total_medals = arma_forecast_by_country(country_name, year, data)

#     # 如果没有足够数据，跳过该年份
#     if forecast_total_medals is None:
#         continue

#     # 获取实际总奖牌数
#     actual_total_medals = data[(data['Country'] == country_name) & (data['Year'] == year)]['Total'].sum()

#     # 计算残差
#     residual = actual_total_medals - forecast_total_medals

#     # 保存结果
#     results.append({'Year': year, 'Forecast_Total_Medals': forecast_total_medals, 'Actual_Total_Medals': actual_total_medals, 'Residual': residual})

# # 转换为 DataFrame 并输出
# results_df = pd.DataFrame(results)

# # 打印预测结果和残差
# print("\n预测结果与残差:")
# print(results_df)
